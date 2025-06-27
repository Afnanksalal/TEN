import json
import redis.asyncio as redis
import google.generativeai as genai
import asyncio
import hashlib
from typing import List, Dict, Any, Optional

from app.models.schemas import ExitStrategyExplorerInput, ExitStrategyExplorerOutput, ExitStrategy, AcquirerType, ActionItem

class ExitStrategyExplorerService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model

    async def explore_exit_strategies(self, input_data: ExitStrategyExplorerInput) -> ExitStrategyExplorerOutput:
        optional_details = []
        if input_data.current_revenue_usd is not None:
            optional_details.append(f"Current Revenue: ${input_data.current_revenue_usd:,.2f} USD.")
        if input_data.monthly_active_users is not None:
            optional_details.append(f"Monthly Active Users (MAU): {input_data.monthly_active_users:,}.")
        if input_data.competitive_landscape_summary:
            optional_details.append(f"Competitive Landscape Summary: {input_data.competitive_landscape_summary}.")
        if input_data.ip_status:
            optional_details.append(f"Intellectual Property Status: {input_data.ip_status}.")
        if input_data.unique_value_proposition:
            optional_details.append(f"Unique Value Proposition: {input_data.unique_value_proposition}.")
        if input_data.founder_exit_goals:
            optional_details.append(f"Founder's Exit Goals: {input_data.founder_exit_goals}.")

        optional_details_str = "\n" + "\n".join(optional_details) if optional_details else ""

        prompt = f"""
        You are an AI strategic advisor helping startup founders plan for long-term growth and potential exit strategies.
        Analyze the startup '{input_data.startup_name}' in the '{input_data.industry}' industry.
        Their business model is summarized as: "{input_data.business_model_summary}".
        They are currently at the '{input_data.funding_stage}' funding stage.
        {optional_details_str}

        Based on this information, identify 2-3 most relevant exit strategies (e.g., Acquisition by Strategic Buyer, IPO, Management Buyout, Liquidation).
        For each strategy:
        - Briefly describe it.
        - Identify common types of acquirers or strategic partners for this type of business.
        - List 3-5 key metrics/characteristics that make a company attractive for this specific exit strategy.
        - Suggest 3-5 actionable steps the startup can take NOW to improve readiness for this strategy.

        Also, provide 3-5 general AI tips for long-term strategic planning.

        Provide the output in a JSON format with the following keys:
        {{
            "startup_name": "{input_data.startup_name}",
            "relevant_exit_strategies": [
                {{
                    "strategy_name": "...",
                    "description": "...",
                    "common_acquirer_types": ["...", "..."],
                    "attractiveness_metrics": ["...", "..."],
                    "action_items": ["...", "..."]
                }}
            ],
            "strategic_planning_tips": ["...", "..."]
        }}
        """

        relevant_exit_strategies: List[ExitStrategy] = []
        strategic_planning_tips: List[str] = []

        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            gemini_output_text = response.text.strip()

            # Clean up the JSON string if it's wrapped in markdown
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            gemini_data = json.loads(gemini_output_text)
            
            strategies_raw = gemini_data.get("relevant_exit_strategies", [])
            for s in strategies_raw:
                # Ensure nested lists are correctly parsed and handle potential non-list types
                common_acquirer_types_list = s.get("common_acquirer_types", [])
                if not isinstance(common_acquirer_types_list, list):
                    common_acquirer_types_list = [str(common_acquirer_types_list)] # Wrap in list if not already

                attractiveness_metrics_list = s.get("attractiveness_metrics", [])
                if not isinstance(attractiveness_metrics_list, list):
                    attractiveness_metrics_list = [str(attractiveness_metrics_list)]
                
                action_items_list = s.get("action_items", [])
                if not isinstance(action_items_list, list):
                    action_items_list = [str(action_items_list)]

                relevant_exit_strategies.append(ExitStrategy(
                    strategy_name=s.get("strategy_name", "Unknown Strategy"),
                    description=s.get("description", "N/A"),
                    common_acquirer_types=[AcquirerType(type_name=t) for t in common_acquirer_types_list],
                    attractiveness_metrics=attractiveness_metrics_list,
                    action_items=[ActionItem(item=i) for i in action_items_list]
                ))
            
            strategic_planning_tips = gemini_data.get("strategic_planning_tips", [])

        except json.JSONDecodeError as e:
            print(f"ERROR(Gemini JSON Parse): Exit Strategy Explorer failed to parse AI response: {e}")
            print(f"Faulty AI Output:\n{gemini_output_text}")
            relevant_exit_strategies = [
                ExitStrategy(
                    strategy_name="AI Response Error",
                    description="Could not parse AI guidance. Response format was incorrect.",
                    common_acquirer_types=[],
                    attractiveness_metrics=[],
                    action_items=[ActionItem(item=f"AI returned malformed JSON: {e}.")]
                )
            ]
            strategic_planning_tips = ["AI response format error."]
        except Exception as e:
            print(f"ERROR(Gemini General): Exit Strategy Explorer failed: {e}")
            relevant_exit_strategies = [
                ExitStrategy(
                    strategy_name="AI Service Error",
                    description="Could not generate guidance due to AI service error.",
                    common_acquirer_types=[],
                    attractiveness_metrics=[],
                    action_items=[ActionItem(item=f"AI service encountered an error: {e}. Check API key or service status.")]
                )
            ]
            strategic_planning_tips = ["AI service encountered an error."]

        return ExitStrategyExplorerOutput(
            startup_name=input_data.startup_name,
            relevant_exit_strategies=relevant_exit_strategies,
            strategic_planning_tips=strategic_planning_tips
        )
