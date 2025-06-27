import json
from typing import List, Dict, Any
import redis.asyncio as redis
from app.models.schemas import RiskInput, RiskOutput, RiskFactor # Assuming your models are in app.models.schemas
import hashlib
import google.generativeai as genai
import asyncio

class RiskAnalyzerService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model

    async def analyze_risk(self, input_data: RiskInput) -> RiskOutput:
        input_hash = hashlib.sha256(input_data.json(exclude_none=True).encode('utf-8')).hexdigest()
        cache_key = f"risk_analysis:{input_hash}"

        cached_result_json = await self.redis_client.get(cache_key)
        if cached_result_json:
            print(f"Cache hit for risk analysis: {cache_key}")
            return RiskOutput.parse_raw(cached_result_json)

        # Build the prompt with conditional inclusion of optional fields
        prompt_parts = [
            f"Analyze the following startup's profile and identify its key risk factors, assign a severity level (low, medium, high) to each, and provide actionable mitigation suggestions. Finally, give an overall risk score (0-100, where 100 is extremely high risk) and general recommendations. Be very critical and realistic.\n",
            f"Startup Name: {input_data.startup_name}",
            f"Industry: {input_data.industry}",
            f"Specific Product/Service: {input_data.specific_product_service}",
            f"Estimated Market Size (USD): {input_data.market_size_usd:,}",
            f"Founder Experience (Years): {input_data.founder_experience_years}",
            f"Initial Funding Needed (USD): {input_data.initial_funding_needed_usd:,}"
        ]

        if input_data.has_mvp is not None:
            prompt_parts.append(f"Has MVP: {'Yes' if input_data.has_mvp else 'No'}")
            if input_data.has_mvp and input_data.mvp_stage_description:
                prompt_parts.append(f"MVP Stage Description: {input_data.mvp_stage_description}")
        
        if input_data.intellectual_property_status:
            prompt_parts.append(f"Intellectual Property Status: {input_data.intellectual_property_status}")
            
        if input_data.regulatory_environment:
            prompt_parts.append(f"Regulatory Environment: {input_data.regulatory_environment}")

        if input_data.burn_rate_usd_per_month is not None:
            prompt_parts.append(f"Estimated Monthly Burn Rate (USD): {input_data.burn_rate_usd_per_month:,}")
        
        if input_data.runway_months is not None:
            prompt_parts.append(f"Estimated Runway (Months): {input_data.runway_months}")

        if input_data.num_direct_competitors is not None:
            prompt_parts.append(f"Number of Direct Competitors: {input_data.num_direct_competitors}")
        
        if input_data.competitive_advantage:
            prompt_parts.append(f"Competitive Advantage: {input_data.competitive_advantage}")

        prompt_parts.append("\nConsider how these additional details influence the risk profile, particularly the MVP status (market validation), IP (defensibility), regulatory environment (operational hurdles), financials (sustainability), and competitive landscape (market viability).")

        prompt_parts.append(f"""
        Provide the output in a JSON format with the following structure:
        {{
            "startup_name": "...",
            "overall_risk_score": <float, 0-100>,
            "risk_factors": [
                {{"name": "...", "level": "low|medium|high", "mitigation_suggestion": "..."}}
            ],
            "recommendations": ["...", "..."]
        }}
        """)
        
        prompt = "\n".join(prompt_parts)

        result = None
        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            
            gemini_output_text = response.text.strip()
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            gemini_data = json.loads(gemini_output_text)
            
            result = RiskOutput(
                startup_name=gemini_data.get("startup_name", input_data.startup_name),
                overall_risk_score=float(gemini_data.get("overall_risk_score", 50.0)),
                risk_factors=[RiskFactor(**f) for f in gemini_data.get("risk_factors", [])],
                recommendations=gemini_data.get("recommendations", [])
            )
            
        except Exception as e:
            print(f"Gemini API call failed for risk analysis: {e}. Falling back to simplified output.")
            result = RiskOutput(
                startup_name=input_data.startup_name,
                overall_risk_score=50.0,
                risk_factors=[RiskFactor(name="AI Service Error", level="high", mitigation_suggestion=f"Gemini analysis failed: {e}. Review input or API key.")],
                recommendations=["Could not generate detailed risk analysis due to AI service error."]
            )

        await self.redis_client.setex(cache_key, 3600, result.json())
        print(f"Cached Gemini-driven risk analysis result for: {cache_key}")

        return result