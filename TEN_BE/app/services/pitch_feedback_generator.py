import json
from typing import List, Optional
import redis.asyncio as redis
from app.models.schemas import PitchFeedbackRequest, PitchFeedbackResponse, RiskOutput, ReputationOutput, InvestorMatchOutput
import google.generativeai as genai
import asyncio
import hashlib

class PitchFeedbackGeneratorService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model

    async def generate_feedback(self, request: PitchFeedbackRequest) -> PitchFeedbackResponse:
        # Cache key for the PitchFeedbackResponse
        input_hash = hashlib.sha256(request.json().encode('utf-8')).hexdigest()
        cache_key_feedback = f"pitch_feedback:{input_hash}"

        cached_feedback_json = await self.redis_client.get(cache_key_feedback)
        if cached_feedback_json:
            print(f"DEBUG(Feedback): Cache hit for pitch feedback: {cache_key_feedback}")
            return PitchFeedbackResponse.parse_raw(cached_feedback_json)

        # Proceed with actual generation if not cached
        risk_info = request.risk_profile.model_dump_json() if request.risk_profile else "Not provided."
        reputation_info = request.reputation_profile.model_dump_json() if request.reputation_profile else "Not provided."
        investor_match_info = request.investor_match_results.model_dump_json() if request.investor_match_results else "Not provided."

        prompt = f"""
        You are an AI startup advisor. Analyze the following pitch for "{request.startup_name}" and provide constructive feedback and actionable suggestions for improvement.
        Focus on clarity, completeness, investor appeal, and addressing potential concerns.
        Consider the following additional context if provided:

        --- Pitch Text ---
        {request.pitch_text}
        --- End Pitch Text ---

        --- Risk Profile (Optional Context) ---
        {risk_info}
        --- End Risk Profile ---

        --- Reputation Profile (Optional Context) ---
        {reputation_info}
        --- End Reputation Profile ---

        --- Investor Match Results (Optional Context) ---
        {investor_match_info}
        --- End Investor Match Results ---

        Provide the output in a JSON format with two keys: "feedback" (list of general observations/strengths) and "suggestions_for_improvement" (list of actionable steps).
        Ensure the suggestions are specific and directly related to the pitch and provided contexts.
        Do not include any preamble, just the JSON.
        """

        feedback_list: List[str] = []
        suggestions: List[str] = []

        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            gemini_output_text = response.text.strip()

            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            gemini_data = json.loads(gemini_output_text)

            feedback_list = gemini_data.get("feedback", ["Gemini did not provide specific feedback. Check prompt or response."])
            suggestions = gemini_data.get("suggestions_for_improvement", ["Gemini did not provide specific suggestions. Check prompt or response."])

        except Exception as e:
            print(f"Gemini API call failed for pitch feedback: {e}")
            feedback_list = ["Could not generate detailed pitch feedback due to AI service error."]
            suggestions = [f"Please check your Google API key or the Gemini service status. Error: {e}"]

        result = PitchFeedbackResponse(
            startup_name=request.startup_name,
            feedback=feedback_list,
            suggestions_for_improvement=suggestions
        )
        # Cache the final PitchFeedbackResponse for 1 hour
        await self.redis_client.setex(cache_key_feedback, 3600, result.json())
        print(f"DEBUG(Feedback): Cached final pitch feedback result: {cache_key_feedback}")

        return result