import json
import redis.asyncio as redis
import google.generativeai as genai
from serpapi import GoogleSearch
import asyncio
import hashlib
import re
from pydantic import HttpUrl
from typing import List, Dict, Any, Optional

from app.models.schemas import CompetitorRadarInput, CompetitorRadarOutput, CompetitorInfo
from app.core.config import settings

class CompetitorRadarService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model
        self.serpapi_key = settings.SERPAPI_API_KEY
        print(f"DEBUG(SerpAPI): Competitor Radar Key loaded status: {bool(self.serpapi_key)}")
        if self.serpapi_key:
            print(f"DEBUG(SerpAPI): Competitor Radar Key prefix: {self.serpapi_key[:5]}...")

    async def _search_google_news(self, query: str) -> List[Dict[str, Any]]:
        if not self.serpapi_key:
            return []

        cache_key = f"news_search:{hashlib.sha256(query.encode('utf-8')).hexdigest()}"
        cached_results = await self.redis_client.get(cache_key)
        if cached_results:
            print(f"DEBUG(SerpAPI): News cache hit for '{query}'.")
            return json.loads(cached_results)

        params = {
            "api_key": self.serpapi_key,
            "engine": "google",
            "q": query,
            "tbm": "nws",
            "gl": "us",
            "hl": "en"
        }
        try:
            search = GoogleSearch(params)
            results = await asyncio.to_thread(search.get_dict)
            news_results = results.get("news_results", [])
            
            await self.redis_client.setex(cache_key, 7200, json.dumps(news_results))
            print(f"DEBUG(SerpAPI): Fetched and cached {len(news_results)} news results for '{query}'.")
            return news_results
        except Exception as e:
            print(f"ERROR(SerpAPI): News search failed for '{query}': {e}")
            return []

    async def _analyze_competitor_with_gemini(self, competitor_name: str, industry: str, news_data: List[Dict[str, Any]]) -> CompetitorInfo:
        prompt_parts = [
            f"Analyze the following news and search results for a competitor named '{competitor_name}' in the '{industry}' industry. ",
            "Extract key information regarding their product/service description, value proposition, target market, recent funding rounds, press mentions, and any indications of hiring surges. ",
            "Provide a concise overall summary of their recent activity.",
            "\n\nNews Data:\n"
        ]
        if news_data:
            for item in news_data[:5]:
                prompt_parts.append(f"- Title: {item.get('title', 'N/A')}\n  Snippet: {item.get('snippet', 'N/A')}\n  Link: {item.get('link', 'N/A')}\n")
        else:
            prompt_parts.append("No specific news found. Synthesize general info.")

        prompt_parts.append("""
        Provide the output in a JSON format with the following keys:
        {
            "name": "Competitor Name",
            "website": "Optional Website URL (extract from links if prominent, otherwise null)",
            "product_description": "Brief description of their product/service.",
            "value_proposition": "Key value proposition they offer.",
            "target_market": "Their primary target market.",
            "funding_rounds": ["Round X: $Y from Z"],
            "press_mentions_summary": ["Summary of key news mentions"],
            "hiring_surge_indication": "High|Medium|Low|No indication" (based on mentions of growth, hiring, expansion),
            "overall_summary": "Concise overview of recent activity."
        }
        If no information is found for a field, provide an empty list, null, or "No indication".
        """)

        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, "".join(prompt_parts))
            gemini_output_text = response.text.strip()
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            gemini_data = json.loads(gemini_output_text)
            
            return CompetitorInfo(
                name=gemini_data.get("name", competitor_name),
                website=gemini_data.get("website"),
                product_description=gemini_data.get("product_description"),
                value_proposition=gemini_data.get("value_proposition"),
                target_market=gemini_data.get("target_market"),
                funding_rounds=gemini_data.get("funding_rounds", []),
                press_mentions_summary=gemini_data.get("press_mentions_summary", []),
                hiring_surge_indication=gemini_data.get("hiring_surge_indication", "No indication"),
                overall_summary=gemini_data.get("overall_summary", "Could not generate detailed summary.")
            )
        except Exception as e:
            print(f"ERROR(Gemini): Competitor analysis failed for '{competitor_name}': {e}")
            return CompetitorInfo(
                name=competitor_name,
                website=None,
                product_description=None,
                value_proposition=None,
                target_market=None,
                funding_rounds=["AI analysis failed"],
                press_mentions_summary=["AI analysis failed"],
                hiring_surge_indication="Error",
                overall_summary=f"Could not generate AI summary due to error: {e}"
            )


    async def track_competitors(self, input_data: CompetitorRadarInput) -> CompetitorRadarOutput:
        search_queries = [
            f"'{input_data.your_industry}' companies for '{input_data.your_product_service_description}'",
            f"competitors of '{input_data.startup_name}' {input_data.your_industry}",
            f"top '{input_data.your_industry}' startups with '{input_data.your_product_service_description}'"
        ]
        
        potential_competitor_candidates = set()
        for query in search_queries:
            google_results = await asyncio.to_thread(GoogleSearch({"api_key": self.serpapi_key, "q": query, "gl": "us", "hl": "en"}).get_dict)
            if "knowledge_graph" in google_results:
                name = google_results["knowledge_graph"].get("title")
                if name and input_data.startup_name.lower() not in name.lower():
                    potential_competitor_candidates.add((name, google_results["knowledge_graph"].get("website")))

            for organic_result in google_results.get("organic_results", []):
                title = organic_result.get("title", "")
                link = organic_result.get("link", "")
                snippet = organic_result.get("snippet", "")

                candidate_name = ""
                if " - " in title:
                    candidate_name = title.split(" - ")[0].strip()
                elif " | " in title:
                    candidate_name = title.split(" | ")[0].strip()
                elif link and ('.com' in link or '.io' in link or '.co' in link or '.tech' in link):
                    domain_match = re.search(r'https?://(?:www\.)?([a-zA-Z0-9-]+)\.(?:com|io|co|tech)', link)
                    if domain_match:
                        candidate_name = domain_match.group(1).replace('-', ' ').title()
                        if len(candidate_name) > 3 and "company" not in candidate_name.lower():
                            potential_competitor_candidates.add((candidate_name, link))
                            continue

                if candidate_name and len(candidate_name) > 3 and input_data.startup_name.lower() not in candidate_name.lower():
                    if not any(kw in title.lower() for kw in ["best", "top", "list", "vs", "review", "news"]) and \
                       not any(kw in snippet.lower() for kw in ["compare", "guide"]):
                        potential_competitor_candidates.add((candidate_name, link))
            
            if len(potential_competitor_candidates) >= 10:
                break

        print(f"DEBUG(SerpAPI): Found {len(potential_competitor_candidates)} raw competitor candidates.")

        competitor_filter_prompt = f"""
        From the following list of potential company names and their associated URLs, identify and select up to 5 actual, distinct competitor companies for a startup in the '{input_data.your_industry}' industry that offers '{input_data.your_product_service_description}'.
        Exclude generic terms, news articles, lists, and irrelevant entries.
        Only include names that appear to be real companies directly competing or offering similar products/services.

        Potential Candidates (Name, URL):
        {json.dumps(list(potential_competitor_candidates), indent=2)}

        Provide the output as a JSON array of selected competitor names (strings), exactly as they appear in the input list.
        Do not include any preamble, just the JSON array.
        """
        
        filtered_competitor_names: List[str] = []
        try:
            gemini_filter_response = await asyncio.to_thread(self.gemini_model.generate_content, competitor_filter_prompt)
            gemini_filter_text = gemini_filter_response.text.strip()
            if gemini_filter_text.startswith("```json") and gemini_filter_text.endswith("```"):
                gemini_filter_text = gemini_filter_text[len("```json"): -len("```")].strip()
            
            filtered_competitor_names = json.loads(gemini_filter_text)
            if not isinstance(filtered_competitor_names, list):
                filtered_competitor_names = []
            print(f"DEBUG(Gemini): Filtered down to {len(filtered_competitor_names)} actual competitors.")

        except Exception as e:
            print(f"ERROR(Gemini): Competitor filtering failed: {e}. Using raw candidates (less accurate).")
            filtered_competitor_names = [name for name, _ in list(potential_competitor_candidates)[:5]]


        tracked_competitors: List[CompetitorInfo] = []
        general_market_trends: List[str] = []

        competitor_name_to_link = {name: link for name, link in potential_competitor_candidates}

        for comp_name in filtered_competitor_names[:5]:
            comp_link = competitor_name_to_link.get(comp_name)
            
            comp_news = await self._search_google_news(f"{comp_name} {input_data.your_industry} {input_data.your_product_service_description} news funding hiring")
            competitor_info = await self._analyze_competitor_with_gemini(comp_name, input_data.your_industry, comp_news)
            
            if comp_link and not competitor_info.website:
                competitor_info.website = HttpUrl(comp_link)
            
            tracked_competitors.append(competitor_info)

            for news_item in comp_news[:5]:
                general_market_trends.append(news_item.get("snippet", ""))

        if general_market_trends:
            trend_prompt = f"""
            Analyze the following snippets related to competitors in the {input_data.your_industry} industry, specifically concerning products/services like: "{input_data.your_product_service_description}".
            Synthesize 3-5 key emerging market trends, challenges, or opportunities.
            Do not include any preamble, just a JSON array of strings.

            Snippets: {'; '.join(general_market_trends)}
            """
            try:
                trend_response = await asyncio.to_thread(self.gemini_model.generate_content, trend_prompt)
                trend_text = trend_response.text.strip()
                if trend_text.startswith("```json") and trend_text.endswith("```"):
                    trend_text = trend_text[len("```json"): -len("```")].strip()
                
                general_market_trends = json.loads(trend_text)
            except Exception as e:
                print(f"ERROR(Gemini): Market trend analysis failed: {e}")
                general_market_trends = ["Could not generate market trends due to AI error."]


        return CompetitorRadarOutput(
            startup_name=input_data.startup_name,
            tracked_competitors=tracked_competitors,
            general_market_trends=general_market_trends
        )
