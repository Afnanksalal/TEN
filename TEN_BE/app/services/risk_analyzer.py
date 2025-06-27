import json
from typing import List, Dict, Any
import redis.asyncio as redis
from app.models.schemas import RiskInput, RiskOutput, RiskFactor
from pathlib import Path
import hashlib # For creating a hash for caching

class RiskAnalyzerService:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.risk_rules = self._load_risk_rules()

    def _load_risk_rules(self) -> Dict[str, Any]:
        """Loads risk rules from a JSON file."""
        # Adjust path if your data directory is structured differently
        file_path = Path(__file__).parent.parent / "data" / "risk_rules.json"
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {file_path} not found. Using default empty rules.")
            return {"rules": [], "default_risk_level": "low"}

    async def analyze_risk(self, input_data: RiskInput) -> RiskOutput:
        """
        Analyzes a startup's risk profile based on predefined rules.
        Includes a basic Redis cache for repeated identical analyses.
        """
        # Create a unique key for caching based on input data
        input_hash = hashlib.sha256(input_data.json().encode('utf-8')).hexdigest()
        cache_key = f"risk_analysis:{input_hash}"

        # Try to retrieve from cache
        cached_result_json = await self.redis_client.get(cache_key)
        if cached_result_json:
            print(f"Cache hit for risk analysis: {cache_key}")
            return RiskOutput.parse_raw(cached_result_json)

        # If not in cache, perform analysis
        risk_factors: List[RiskFactor] = []
        overall_risk_score = 0.0 # Max possible score for sum of rules is 75 in current logic
        recommendations: List[str] = []

        # Example rule-based assessment (can be expanded/made more complex)
        # Using specific values for hackathon simplicity, replace with data from risk_rules.json if time permits
        
        # Market Size Risk
        if input_data.market_size_usd < 500_000_000:
            risk_factors.append(RiskFactor(name="Market Size", level="high", mitigation_suggestion="Conduct deeper market research or explore niche expansion."))
            overall_risk_score += 30
            recommendations.append("Your target market appears small. Consider expanding your total addressable market or focusing on a highly underserved niche.")
        elif input_data.market_size_usd < 1_000_000_000:
            risk_factors.append(RiskFactor(name="Market Size", level="medium", mitigation_suggestion="Validate market demand with early customers."))
            overall_risk_score += 15
        else:
            risk_factors.append(RiskFactor(name="Market Size", level="low", mitigation_suggestion="Maintain market awareness."))
            overall_risk_score += 5

        # Team Experience Risk
        if input_data.founder_experience_years < 2:
            risk_factors.append(RiskFactor(name="Team Experience", level="high", mitigation_suggestion="Seek experienced mentors or co-founders."))
            overall_risk_score += 25
            recommendations.append("Limited founder experience detected. Actively seek mentors, advisors, or experienced co-founders to bolster your team.")
        elif input_data.founder_experience_years < 5:
            risk_factors.append(RiskFactor(name="Team Experience", level="medium", mitigation_suggestion="Focus on continuous learning and networking."))
            overall_risk_score += 10
        else:
            risk_factors.append(RiskFactor(name="Team Experience", level="low", mitigation_suggestion="Leverage experience for strategic advantage."))
            overall_risk_score += 3

        # Funding Requirement Risk
        if input_data.initial_funding_needed_usd > 1_000_000:
            risk_factors.append(RiskFactor(name="Funding Requirement", level="high", mitigation_suggestion="Prepare a detailed financial model and clear use of funds."))
            overall_risk_score += 20
            recommendations.append("High initial funding requirement. Ensure you have a robust financial plan and clear milestones for investor confidence.")
        elif input_data.initial_funding_needed_usd > 200_000:
            risk_factors.append(RiskFactor(name="Funding Requirement", level="medium", mitigation_suggestion="Optimize initial burn rate."))
            overall_risk_score += 10
        else:
            risk_factors.append(RiskFactor(name="Funding Requirement", level="low", mitigation_suggestion="Focus on efficient capital deployment."))
            overall_risk_score += 5

        # Normalize overall_risk_score to a 0-100 scale (max possible sum of highest risks is 75)
        # Using a fixed max for normalization, adjust if you add more rules
        MAX_POSSIBLE_SCORE = 75 # 30 (market) + 25 (team) + 20 (funding)
        normalized_score = min(overall_risk_score / MAX_POSSIBLE_SCORE * 100, 100)

        result = RiskOutput(
            startup_name=input_data.startup_name,
            overall_risk_score=round(normalized_score, 2),
            risk_factors=risk_factors,
            recommendations=recommendations
        )

        # Cache the result for 1 hour (3600 seconds)
        await self.redis_client.setex(cache_key, 3600, result.json())
        print(f"Cached risk analysis result for: {cache_key}")

        return result