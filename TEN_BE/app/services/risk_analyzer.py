import json
from typing import List, Dict, Any
import redis.asyncio as redis
from app.models.schemas import RiskInput, RiskOutput, RiskFactor
import hashlib
import google.generativeai as genai
import asyncio

class RiskAnalyzerService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model

    async def analyze_risk(self, input_data: RiskInput) -> RiskOutput:
        input_hash = hashlib.sha256(input_data.json().encode('utf-8')).hexdigest()
        cache_key = f"risk_analysis:{input_hash}"

        cached_result_json = await self.redis_client.get(cache_key)
        if cached_result_json:
            print(f"Cache hit for risk analysis: {cache_key}")
            return RiskOutput.parse_raw(cached_result_json)

        prompt = f"""
        Analyze the following startup's profile and identify its key risk factors, assign a severity level (low, medium, high) to each, and provide actionable mitigation suggestions. Finally, give an overall risk score (0-100, where 100 is extremely high risk) and general recommendations. Be very critical and realistic.

        Startup Name: {input_data.startup_name}
        Industry: {input_data.industry}
        Estimated Market Size (USD): {input_data.market_size_usd:,}
        Founder Experience (Years): {input_data.founder_experience_years}
        Initial Funding Needed (USD): {input_data.initial_funding_needed_usd:,}

        Provide the output in a JSON format with the following structure:
        {{
            "startup_name": "...",
            "overall_risk_score": <float, 0-100>,
            "risk_factors": [
                {{"name": "...", "level": "low|medium|high", "mitigation_suggestion": "..."}}
            ],
            "recommendations": ["...", "..."]
        }}
        """

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