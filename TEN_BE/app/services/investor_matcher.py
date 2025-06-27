import json
from typing import List, Dict, Any, Optional
import redis.asyncio as redis
from app.models.schemas import InvestorMatchInput, InvestorMatchOutput, MatchDetail, InvestorProfile, RiskOutput, ReputationOutput
import google.generativeai as genai
import asyncio
import hashlib
from serpapi import GoogleSearch
from app.core.config import settings

class InvestorMatcherService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model
        self.serpapi_key = settings.SERPAPI_API_KEY
        if not self.serpapi_key:
            print("WARNING: SerpAPI key not configured for InvestorMatcher. Investor search will be limited or fail.")


    async def _generate_investor_search_queries(self, input_data: InvestorMatchInput) -> List[str]:
        prompt = f"""
        Given the following startup profile, generate 3-5 highly effective Google search queries to find suitable actual investors (angel investors, venture capital firms, accelerators).
        Focus on keywords related to industry, funding stage, and risk tolerance. Do NOT include phrases like 'site:twitter.com'.
        Examples: 'seed stage AI venture capital', 'early stage healthtech angel investors', 'climate tech series A VCs'.

        Startup Name: {input_data.startup_name}
        Industry: {input_data.industry}
        Funding Sought (USD): {input_data.funding_sought_usd:,}
        Overall Risk Score: {input_data.risk_profile.overall_risk_score}
        Key Risk Factors: {', '.join([f'{f.name} ({f.level})' for f in input_data.risk_profile.risk_factors])}

        Provide the output as a JSON array of strings: ["query1", "query2", "query3"]
        """
        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            gemini_output_text = response.text.strip()
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            queries = json.loads(gemini_output_text)
            if not isinstance(queries, list) or not all(isinstance(q, str) for q in queries):
                raise ValueError("Gemini did not return a valid list of queries.")
            print(f"DEBUG(Matching): Generated queries: {queries}")
            return queries
        except Exception as e:
            print(f"ERROR(Matching): Gemini failed to generate investor search queries: {e}")
            return [
                f"{input_data.industry} angel investors",
                f"seed stage {input_data.industry} VC firms",
                f"accelerators for {input_data.industry} startups"
            ]

    async def _fetch_investors_from_serpapi(self, query: str) -> List[Dict[str, Any]]:
        """
        Fetches Google search results for investor queries using SerpAPI.
        Extracts relevant snippets and titles.
        """
        if not self.serpapi_key:
            print("SerpAPI key not configured. Skipping investor search via SerpAPI.")
            return []

        cache_key_serp = f"investor_serp_raw:{hashlib.sha256(query.encode('utf-8')).hexdigest()}"
        cached_results_json = await self.redis_client.get(cache_key_serp)
        if cached_results_json:
            print(f"DEBUG(Matching): Cache hit for investor SerpAPI raw results: '{query}'")
            return json.loads(cached_results_json)

        params = {
            "api_key": self.serpapi_key,
            "engine": "google",
            "q": query,
            "num": 10
        }
        results_data = []
        try:
            print(f"DEBUG(Matching): Calling SerpAPI for investor query '{query}' with params: {params}")
            search = GoogleSearch(params)
            raw_results = await asyncio.to_thread(search.get_dict)
            
            if "error" in raw_results:
                print(f"ERROR(Matching): SerpAPI returned an error for investor query '{query}': {raw_results['error']}")
                return []

            if "organic_results" in raw_results:
                for res in raw_results["organic_results"]:
                    results_data.append({
                        "title": res.get("title", ""),
                        "link": res.get("link", ""),
                        "snippet": res.get("snippet", "")
                    })
            
            if results_data:
                await self.redis_client.setex(cache_key_serp, 3600, json.dumps(results_data))
                print(f"DEBUG(Matching): Cached {len(results_data)} raw search results for '{query}'.")
            else:
                print(f"DEBUG(Matching): No organic results found for investor query '{query}'. Not caching.")

        except Exception as e:
            print(f"ERROR(Matching): Exception during SerpAPI investor call for query '{query}': {type(e).__name__}: {e}")
        return results_data

    async def _curate_investors_with_gemini(self, startup_info: Dict[str, Any], raw_investor_results: List[Dict[str, Any]]) -> List[MatchDetail]:
        """
        Uses Gemini to identify, filter, and rank actual investors from raw search results.
        Limited to a maximum of 3 investors.
        """
        if not raw_investor_results:
            return []

        clean_results = []
        for res in raw_investor_results:
            link = res.get("link", "").lower()
            if not any(domain in link for domain in ["wikipedia.org", "youtube.com", "linkedin.com", "twitter.com", "facebook.com", "crunchbase.com", "medium.com", "news.", "blog."]) and \
               ("investor" in res.get("snippet", "").lower() or "fund" in res.get("snippet", "").lower() or "capital" in res.get("title", "").lower() or "vc" in res.get("title", "").lower() or "angel" in res.get("title", "").lower()): # Added more keywords for filtering
                clean_results.append(res)
        
        top_n_results = clean_results[:10]

        prompt = f"""
        You are an expert in startup funding. Given the following startup's profile and a list of Google search results,
        identify the 3 MOST RELEVANT and ACTUAL investors (can be a specific firm, an angel investor, or an accelerator) that would be a good match for this startup.
        For each identified investor, provide:
        - Their specific name (firm or individual).
        - Their website link (if available from results).
        - A match score (0-100).
        - Concise reasons for the match.
        - Any significant gaps (why they might NOT be a perfect fit or what the startup needs to do).
        - Their inferred risk tolerance (low, medium, high).
        - Their inferred preferred industries (list of strings).
        - Their inferred typical min/max investment in USD (integer).
        - Their inferred feedback focus (list of strings).

        Startup Profile:
        {json.dumps(startup_info, indent=2)}

        Google Search Results:
        ```json
        {json.dumps(top_n_results, indent=2)}
        ```

        Provide the output in a JSON array of matched investor objects, strictly adhering to the MatchDetail schema (with InvestorProfile embedded).
        Only include investors you can confidently identify and assign values to. Max 3 investors.
        Example of expected output structure for one investor:
        {{
            "investor": {{
                "id": "firm_xyz",
                "name": "Firm XYZ Ventures",
                "link": "https://firmxyz.com",
                "risk_tolerance": "high",
                "preferred_industries": ["AI", "SaaS"],
                "min_investment_usd": 1000000,
                "max_investment_usd": 10000000,
                "feedback_focus": ["Traction", "Team"]
            }},
            "match_score": 90,
            "match_reasons": ["Strong focus on AI startups", "Matches funding stage"],
            "gaps": ["Prefers later stage, need more revenue"]
        }}
        Do not include any preamble, just the JSON array.
        """
        
        matched_details: List[MatchDetail] = []
        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            gemini_output_text = response.text.strip()
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            gemini_curated_data = json.loads(gemini_output_text)
            
            for item in gemini_curated_data:
                investor_profile_data = item.get("investor", {})
                if not investor_profile_data.get("name") or not investor_profile_data.get("link"):
                    continue
                
                investor_id = hashlib.sha256(investor_profile_data.get("link", investor_profile_data["name"]).encode('utf-8')).hexdigest()[:10]
                
                investor_profile = InvestorProfile(
                    id=investor_id,
                    name=investor_profile_data["name"],
                    link=investor_profile_data.get("link"),
                    risk_tolerance=investor_profile_data.get("risk_tolerance", "medium"),
                    preferred_industries=investor_profile_data.get("preferred_industries", [startup_info.get("industry", "Any")]),
                    min_investment_usd=investor_profile_data.get("min_investment_usd", 100000),
                    max_investment_usd=investor_profile_data.get("max_investment_usd", 5000000),
                    feedback_focus=investor_profile_data.get("feedback_focus", ["Overall Fit"])
                )
                matched_details.append(MatchDetail(
                    investor=investor_profile,
                    match_score=float(item.get("match_score", 0)),
                    match_reasons=item.get("match_reasons", []),
                    gaps=item.get("gaps", [])
                ))
                if len(matched_details) >= 3:
                    break
            
            return matched_details

        except Exception as e:
            print(f"ERROR(Matching): Gemini failed to curate investors: {e}")
            return []


    async def match_investors(self, input_data: InvestorMatchInput) -> InvestorMatchOutput:
        input_hash = hashlib.sha256(input_data.json().encode('utf-8')).hexdigest()
        cache_key_matching = f"investor_matching:{input_hash}"

        cached_matching_json = await self.redis_client.get(cache_key_matching)
        if cached_matching_json:
            print(f"DEBUG(Matching): Cache hit for investor matching: {cache_key_matching}")
            return InvestorMatchOutput.parse_raw(cached_matching_json)

        queries = await self._generate_investor_search_queries(input_data)
        
        all_raw_investor_results = []
        for q in queries:
            raw_results = await self._fetch_investors_from_serpapi(q)
            all_raw_investor_results.extend(raw_results)
        
        deduplicated_results = {}
        for res in all_raw_investor_results:
            if res.get("link"):
                deduplicated_results[res["link"]] = res
            elif res.get("title"):
                deduplicated_results[res["title"]] = res
        
        final_raw_results = list(deduplicated_results.values())

        startup_info = {
            "startup_name": input_data.startup_name,
            "industry": input_data.industry,
            "funding_sought_usd": input_data.funding_sought_usd,
            "risk_profile": input_data.risk_profile.model_dump(),
            "reputation_profile": input_data.reputation_profile.model_dump()
        }
        matched_investors_list = await self._curate_investors_with_gemini(startup_info, final_raw_results)
        
        if not matched_investors_list:
            matched_investors_list = [
                MatchDetail(
                    investor=InvestorProfile(
                        id="fallback_02",
                        name="No Specific Investors Found (AI Curation Failed)",
                        link=None,
                        risk_tolerance="medium",
                        preferred_industries=[input_data.industry],
                        min_investment_usd=input_data.funding_sought_usd,
                        max_investment_usd=input_data.funding_sought_usd + 1000000,
                        feedback_focus=["General Investor Fit"]
                    ),
                    match_score=0.0,
                    match_reasons=["Could not identify specific investors from public data matching your profile."],
                    gaps=["Try refining your startup's public presence or search terms."]
                )
            ]


        result = InvestorMatchOutput(startup_name=input_data.startup_name, matched_investors=matched_investors_list)
        await self.redis_client.setex(cache_key_matching, 3600, result.json())
        print(f"DEBUG(Matching): Cached final investor matching result: {cache_key_matching}")

        return result
