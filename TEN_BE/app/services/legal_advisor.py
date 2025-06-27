import redis.asyncio as redis
import google.generativeai as genai
import asyncio
import json
import hashlib
from typing import List, Dict, Any

from app.models.schemas import LegalAssistanceInput, LegalAssistanceOutput, LegalDocument, LicenseCertification, LegalRisk

class LegalAdvisorService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model

    async def get_legal_assistance(self, input_data: LegalAssistanceInput) -> LegalAssistanceOutput:
        input_hash = hashlib.sha256(input_data.json().encode('utf-8')).hexdigest()
        cache_key = f"legal_assistance:{input_hash}"

        cached_result_json = await self.redis_client.get(cache_key)
        if cached_result_json:
            print(f"Cache hit for legal assistance: {cache_key}")
            return LegalAssistanceOutput.parse_raw(cached_result_json)

        prompt = f"""
        You are an AI legal assistant specializing in startup law. Based on the following startup profile,
        identify essential legal documents, required industry-specific licenses/certifications, and key legal risks with prevention strategies.
        Provide general legal advice relevant to their stage.

        Startup Name: {input_data.startup_name}
        Industry: {input_data.industry}
        Business Model Summary: {input_data.business_model_summary}
        Funding Stage: {input_data.funding_stage}
        Number of Founders: {input_data.num_founders}
        Number of Employees: {input_data.num_employees}
        Handles Personal Data: {input_data.handles_personal_data}
        Sells Physical Products: {input_data.sells_physical_products}

        Provide the output in a JSON format with the following structure:
        {{
            "startup_name": "...",
            "essential_documents": [
                {{"name": "...", "description": "...", "relevance_reason": "..."}}
            ],
            "industry_licenses_certs": [
                {{"name": "...", "description": "...", "relevance_reason": "..."}}
            ],
            "key_legal_risks": [
                {{"name": "...", "description": "...", "prevention_strategy": "..."}}
            ],
            "general_legal_advice": ["...", "..."]
        }}
        Ensure all lists are comprehensive and relevant to the startup's profile.
        Do not include any preamble, just the JSON.
        """

        result = None
        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            gemini_output_text = response.text.strip()
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            gemini_data = json.loads(gemini_output_text)
            
            result = LegalAssistanceOutput(
                startup_name=gemini_data.get("startup_name", input_data.startup_name),
                essential_documents=[LegalDocument(**d) for d in gemini_data.get("essential_documents", [])],
                industry_licenses_certs=[LicenseCertification(**lc) for lc in gemini_data.get("industry_licenses_certs", [])],
                key_legal_risks=[LegalRisk(**lr) for lr in gemini_data.get("key_legal_risks", [])],
                general_legal_advice=gemini_data.get("general_legal_advice", [])
            )
            
        except Exception as e:
            print(f"Gemini API call failed for legal assistance: {e}. Falling back to simplified output.")
            result = LegalAssistanceOutput(
                startup_name=input_data.startup_name,
                essential_documents=[],
                industry_licenses_certs=[],
                key_legal_risks=[LegalRisk(name="AI Service Error", description="Legal advice could not be generated.", prevention_strategy=f"Gemini error: {e}. Check API key or service.")],
                general_legal_advice=["Could not generate detailed legal assistance due to AI service error."]
            )

        await self.redis_client.setex(cache_key, 3600, result.json())
        print(f"Cached Gemini-driven legal assistance result for: {cache_key}")

        return result