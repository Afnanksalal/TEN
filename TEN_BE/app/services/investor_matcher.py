import json
from typing import List, Dict, Any
import redis.asyncio as redis
from app.models.schemas import InvestorMatchInput, InvestorMatchOutput, MatchDetail, InvestorProfile, RiskOutput, ReputationOutput
from pathlib import Path

class InvestorMatcherService:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.investor_profiles = self._load_investor_profiles()

    def _load_investor_profiles(self) -> List[Dict[str, Any]]:
        """Loads investor profiles from a JSON file."""
        file_path = Path(__file__).parent.parent / "data" / "investor_profiles.json"
        try:
            with open(file_path, "r") as f:
                return [InvestorProfile(**profile_data) for profile_data in json.load(f)]
        except FileNotFoundError:
            print(f"Warning: {file_path} not found. Returning empty investor profiles.")
            return []

    async def match_investors(self, input_data: InvestorMatchInput) -> InvestorMatchOutput:
        """
        Matches a startup with potential investor profiles based on various criteria
        including risk, industry, funding, and sentiment.
        """
        matched_results: List[MatchDetail] = []

        # Extract relevant data from input
        startup_risk_score = input_data.risk_profile.overall_risk_score
        startup_industry = input_data.industry
        startup_funding_needed = input_data.funding_sought_usd
        startup_sentiment_score = input_data.reputation_profile.overall_sentiment_score

        for investor_profile in self.investor_profiles:
            match_score = 0.0
            match_reasons = []
            gaps = []

            # 1. Industry Match (Strongest factor)
            if startup_industry.lower() in [i.lower() for i in investor_profile.preferred_industries]:
                match_score += 0.4 # Higher weight for industry
                match_reasons.append(f"Strong industry alignment: {startup_industry}")
            else:
                gaps.append(f"Industry mismatch: Investor typically prefers {', '.join(investor_profile.preferred_industries)}.")

            # 2. Funding Range Match
            if investor_profile.min_investment_usd <= startup_funding_needed <= investor_profile.max_investment_usd:
                match_score += 0.3
                match_reasons.append(f"Funding range matches investor's typical ticket size ({investor_profile.min_investment_usd:,} - {investor_profile.max_investment_usd:,} USD).")
            else:
                gaps.append(f"Funding range mismatch: You seek {startup_funding_needed:,} USD, investor's range is {investor_profile.min_investment_usd:,} - {investor_profile.max_investment_usd:,} USD.")

            # 3. Risk Tolerance Match (simple mapping)
            # Higher risk score means more "high" risk, lower means "low" risk
            risk_match = False
            if startup_risk_score >= 60 and investor_profile.risk_tolerance == "high":
                risk_match = True
            elif 30 <= startup_risk_score < 60 and investor_profile.risk_tolerance == "medium":
                risk_match = True
            elif startup_risk_score < 30 and investor_profile.risk_tolerance == "low":
                risk_match = True

            if risk_match:
                match_score += 0.2
                match_reasons.append(f"Risk tolerance alignment: Your risk profile ({round(startup_risk_score)}%) aligns with investor's appetite for '{investor_profile.risk_tolerance}' risk.")
            else:
                gaps.append(f"Risk tolerance mismatch: Your risk profile ({round(startup_risk_score)}%) might not align with investor's '{investor_profile.risk_tolerance}' tolerance.")

            # 4. Sentiment Consideration (bonus points for very positive, penalty for very negative)
            if startup_sentiment_score > 0.7: # Very positive
                match_score += 0.1
                match_reasons.append("Very strong positive early sentiment detected. Great for investor confidence!")
            elif startup_sentiment_score < -0.7: # Very negative
                match_score -= 0.2 # Heavier penalty for very negative sentiment
                gaps.append("Significant negative early sentiment detected. This will be a major concern for investors.")
            elif startup_sentiment_score > 0.3: # Moderately positive
                match_score += 0.05
                match_reasons.append("Moderately positive early sentiment. A good start.")


            # Only include matches with a positive overall score
            if match_score > 0.0:
                matched_results.append(
                    MatchDetail(
                        investor=investor_profile,
                        match_score=round(match_score * 100, 2), # Convert to percentage for clarity
                        match_reasons=match_reasons,
                        gaps=gaps
                    )
                )
        
        # Sort by match score, descending
        matched_results.sort(key=lambda x: x.match_score, reverse=True)

        return InvestorMatchOutput(startup_name=input_data.startup_name, matched_investors=matched_results)