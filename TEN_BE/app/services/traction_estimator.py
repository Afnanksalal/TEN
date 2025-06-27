import json
import redis.asyncio as redis
import google.generativeai as genai
import asyncio
import hashlib
from typing import List, Dict, Any, Optional

from app.models.schemas import TractionEstimatorInput, TractionEstimatorOutput, TractionBenchmark

class TractionEstimatorService:
    def __init__(self, redis_client: redis.Redis, gemini_model: genai.GenerativeModel):
        self.redis_client = redis_client
        self.gemini_model = gemini_model

    async def estimate_traction(self, input_data: TractionEstimatorInput) -> TractionEstimatorOutput:
        industry_benchmarks = {
            "SaaS": {
                "monthly_active_users": 10000, "monthly_recurring_revenue_usd": 50000,
                "customer_acquisition_cost_usd": 150, "customer_lifetime_value_usd": 1500,
                "churn_rate_percent": 5.0, "conversion_rate_percent": 2.0
            },
            "eCommerce": {
                "monthly_active_users": 50000, "monthly_recurring_revenue_usd": 75000,
                "customer_acquisition_cost_usd": 50, "customer_lifetime_value_usd": 500,
                "churn_rate_percent": 10.0, "conversion_rate_percent": 3.0
            },
            "HealthTech": {
                "monthly_active_users": 2000, "monthly_recurring_revenue_usd": 20000,
                "customer_acquisition_cost_usd": 300, "customer_lifetime_value_usd": 3000,
                "churn_rate_percent": 3.0, "conversion_rate_percent": 1.0
            },
            "AI": {
                "monthly_active_users": 5000, "monthly_recurring_revenue_usd": 60000,
                "customer_acquisition_cost_usd": 200, "customer_lifetime_value_usd": 2000,
                "churn_rate_percent": 4.0, "conversion_rate_percent": 1.5
            }
        }

        benchmark_data = industry_benchmarks.get(input_data.your_industry, industry_benchmarks["SaaS"])

        benchmarks: List[TractionBenchmark] = []
        growth_health_score_components = []

        metrics_map = {
            "monthly_active_users": "Monthly Active Users",
            "monthly_recurring_revenue_usd": "Monthly Recurring Revenue (USD)",
            "customer_acquisition_cost_usd": "Customer Acquisition Cost (USD)",
            "customer_lifetime_value_usd": "Customer Lifetime Value (USD)",
            "churn_rate_percent": "Churn Rate (%)",
            "conversion_rate_percent": "Conversion Rate (%)"
        }

        for metric_key, metric_name in metrics_map.items():
            your_value = getattr(input_data, metric_key, None)
            industry_avg = benchmark_data.get(metric_key)
            comparison_text = "N/A"
            score_contribution = 0

            if your_value is not None and industry_avg is not None:
                if metric_key in ["customer_acquisition_cost_usd", "churn_rate_percent"]:
                    if your_value < industry_avg * 0.8: comparison_text = "Significantly better than average"; score_contribution = 20
                    elif your_value < industry_avg: comparison_text = "Better than average"; score_contribution = 10
                    elif your_value > industry_avg * 1.2: comparison_text = "Significantly worse than average"; score_contribution = -20
                    elif your_value > industry_avg: comparison_text = "Worse than average"; score_contribution = -10
                    else: comparison_text = "Around industry average"; score_contribution = 5
                else:
                    if your_value > industry_avg * 1.2: comparison_text = "Significantly better than average"; score_contribution = 20
                    elif your_value > industry_avg: comparison_text = "Better than average"; score_contribution = 10
                    elif your_value < industry_avg * 0.8: comparison_text = "Significantly worse than average"; score_contribution = -20
                    elif your_value < industry_avg: comparison_text = "Worse than average"; score_contribution = -10
                    else: comparison_text = "Around industry average"; score_contribution = 5
            else:
                comparison_text = "Not provided, cannot benchmark"
                score_contribution = 0

            benchmarks.append(TractionBenchmark(
                metric=metric_name,
                your_value=your_value,
                industry_average=industry_avg,
                comparison=comparison_text
            ))
            if your_value is not None:
                growth_health_score_components.append(score_contribution)

        if growth_health_score_components:
            avg_contribution = sum(growth_health_score_components) / len(growth_health_score_components)
            growth_health_score = ((avg_contribution + 20) / 40) * 100
            growth_health_score = max(0, min(100, growth_health_score))
        else:
            growth_health_score = 50.0

        prompt = f"""
        Analyze the following growth metrics and benchmarks for the startup '{input_data.startup_name}' in the '{input_data.your_industry}' industry.
        Provide 3-5 actionable insights and tips for improving their traction based on these numbers.
        If a metric is missing, suggest what insight it could provide.

        --- Metrics & Benchmarks ---
        {json.dumps([b.model_dump() for b in benchmarks], indent=2)}
        --- End Metrics & Benchmarks ---

        Provide the output in a JSON array of strings, with each string being an actionable insight.
        Do not include any preamble, just the JSON array.
        """
        ai_insights: List[str] = []
        try:
            response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
            gemini_output_text = response.text.strip()
            if gemini_output_text.startswith("```json") and gemini_output_text.endswith("```"):
                gemini_output_text = gemini_output_text[len("```json"): -len("```")].strip()
            
            ai_insights = json.loads(gemini_output_text)
            if not isinstance(ai_insights, list):
                ai_insights = [str(ai_insights)]
        except Exception as e:
            print(f"ERROR(Gemini): Traction estimator insights failed: {e}")
            ai_insights = ["Could not generate traction insights due to AI error."]


        return TractionEstimatorOutput(
            startup_name=input_data.startup_name,
            growth_health_score=round(growth_health_score, 2),
            benchmarks=benchmarks,
            ai_insights=ai_insights
        )