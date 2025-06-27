import json
import redis.asyncio as redis
import google.generativeai as genai
import asyncio
import hashlib
from typing import List, Dict, Any, Optional

from app.models.schemas import BuzzBuilderInput, BuzzBuilderOutput, SocialPostSuggestion

class BuzzBuilderService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model

    async def generate_buzz(self, input_data: BuzzBuilderInput) -> BuzzBuilderOutput:
        prompt = f"""
        You are an AI content strategist specializing in startup growth and public relations.
        Generate compelling content suggestions for '{input_data.startup_name}' in the '{input_data.your_industry}' industry.

        Here's the context:
        - Current Milestones: {', '.join(input_data.current_milestones)}
        - Key Message/Narrative: {input_data.key_message}
        - Target Audience: {input_data.target_audience}

        Suggest content for the following platforms:
        1. Twitter Thread (4-5 tweets)
        2. LinkedIn Post
        3. Blog Post Idea (with 3-4 key points)

        For each suggestion, provide a title, key content points (as a list of strings), relevant hashtags (list of strings), and a call to action.
        Finally, provide 3-5 general AI tips for maximizing buzz.

        Provide the output in a JSON format with the following structure:
        {{
            "startup_name": "{input_data.startup_name}",
            "suggestions": [
                {{
                    "platform": "Twitter Thread",
                    "title": "...",
                    "content_points": ["...", "..."],
                    "hashtags": ["#...", "#..."],
                    "call_to_action": "..."
                }},
                {{
                    "platform": "LinkedIn Post",
                    "title": "...",
                    "content_points": ["...", "..."],
                    "hashtags": ["#...", "#..."],
                    "call_to_action": "..."
                }},
                {{
                    "platform": "Blog Post Idea",
                    "title": "...",
                    "content_points": ["...", "..."],
                    "hashtags": ["#...", "#..."],
                    "call_to_action": "..."
                }}
            ],
            "ai_tips": ["...", "..."]
        }}
        """

        suggestions: List[SocialPostSuggestion] = []
        ai_tips: List[str] = []

        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            gemini_output_text = response.text.strip()
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            gemini_data = json.loads(gemini_output_text)
            
            suggestions_raw = gemini_data.get("suggestions", [])
            for s in suggestions_raw:
                suggestions.append(SocialPostSuggestion(**s))
            
            ai_tips = gemini_data.get("ai_tips", [])

        except Exception as e:
            print(f"ERROR(Gemini): Buzz Builder analysis failed: {e}")
            suggestions = [
                SocialPostSuggestion(
                    platform="Error",
                    title="AI Generation Failed",
                    content_points=[f"Could not generate content suggestions due to AI error: {e}"],
                    hashtags=[],
                    call_to_action="Please check API key or service status."
                )
            ]
            ai_tips = ["AI service encountered an error."]

        return BuzzBuilderOutput(
            startup_name=input_data.startup_name,
            suggestions=suggestions,
            ai_tips=ai_tips
        )