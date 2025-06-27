import json
import redis.asyncio as redis
import google.generativeai as genai
import asyncio
import hashlib
from typing import List, Dict, Any, Optional

from app.models.schemas import TalentNavigatorInput, TalentNavigatorOutput, RecommendedRole, InterviewQuestion, TalentTip

class TalentNavigatorService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model

    async def get_talent_guidance(self, input_data: TalentNavigatorInput) -> TalentNavigatorOutput:
        prompt = f"""
        You are an AI talent advisor specializing in startup team building.
        Analyze the startup '{input_data.startup_name}' in the '{input_data.your_industry}' industry, currently at the '{input_data.funding_stage}' funding stage with {input_data.current_team_size} team members.
        Their key challenge is: '{input_data.key_challenge}'.

        Based on this, recommend 3-5 key roles they should consider hiring or bringing on as advisors.
        For each recommended role, describe the ideal candidate profile (key skills, experience, traits).
        Suggest 2-3 specific, insightful interview questions for each role.
        Finally, provide 3-5 general AI coaching tips for building a strong early-stage team.

        Provide the output in a JSON format with the following keys:
        {{
            "startup_name": "{input_data.startup_name}",
            "recommended_roles": [
                {{
                    "role_name": "...",
                    "ideal_candidate_profile": "...",
                    "interview_questions": ["...", "..."]
                }}
            ],
            "team_building_tips": ["...", "..."]
        }}
        """

        recommended_roles: List[RecommendedRole] = []
        team_building_tips: List[TalentTip] = [] # Using TalentTip for consistency if it's just a list of strings

        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            gemini_output_text = response.text.strip()
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            gemini_data = json.loads(gemini_output_text)
            
            roles_raw = gemini_data.get("recommended_roles", [])
            for r in roles_raw:
                # Ensure interview_questions is a list of strings
                interview_q_list = r.get("interview_questions", [])
                if not isinstance(interview_q_list, list):
                    interview_q_list = [str(interview_q_list)] # Convert to list if not already

                recommended_roles.append(RecommendedRole(
                    role_name=r.get("role_name", "Unknown Role"),
                    ideal_candidate_profile=r.get("ideal_candidate_profile", "N/A"),
                    interview_questions=[InterviewQuestion(question=q) for q in interview_q_list] # Wrap each question
                ))
            
            team_building_tips = [TalentTip(tip=t) for t in gemini_data.get("team_building_tips", [])]

        except Exception as e:
            print(f"ERROR(Gemini): Talent Navigator failed: {e}")
            recommended_roles = [
                RecommendedRole(
                    role_name="AI Error",
                    ideal_candidate_profile="Could not generate guidance due to AI service error.",
                    interview_questions=[InterviewQuestion(question="Please check API key or service status.")]
                )
            ]
            team_building_tips = [TalentTip(tip=f"AI service encountered an error: {e}")]

        return TalentNavigatorOutput(
            startup_name=input_data.startup_name,
            recommended_roles=recommended_roles,
            team_building_tips=team_building_tips
        )