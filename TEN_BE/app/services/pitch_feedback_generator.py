from typing import List, Optional
import redis.asyncio as redis
from app.models.schemas import PitchFeedbackRequest, PitchFeedbackResponse, RiskOutput, ReputationOutput, InvestorMatchOutput

class PitchFeedbackGeneratorService:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    async def generate_feedback(self, request: PitchFeedbackRequest) -> PitchFeedbackResponse:
        """
        Generates constructive feedback and suggestions for a startup's pitch.
        Leverages risk and reputation analysis results if available.
        """
        feedback_list: List[str] = []
        suggestions: List[str] = []

        pitch_lower = request.pitch_text.lower()

        # Basic Pitch Structure Checks
        if len(request.pitch_text) < 150:
            feedback_list.append("Pitch is quite short.")
            suggestions.append("Consider expanding on key sections like problem, solution, market, and team. Aim for a concise but comprehensive overview.")
        elif len(request.pitch_text) > 1500:
            feedback_list.append("Pitch might be too long.")
            suggestions.append("Focus on conciseness. Can you convey your core message more efficiently? Investors have limited time.")

        # Check for core pitch elements (simple keyword detection)
        keywords_problem = ["problem", "challenge", "issue", "pain point"]
        keywords_solution = ["solution", "product", "service", "how it works", "platform"]
        keywords_market = ["market", "target audience", "customers", "TAM", "SAM", "SOM"]
        keywords_team = ["team", "founders", "experience", "background"]
        keywords_traction = ["traction", "users", "revenue", "growth", "metrics"]
        keywords_ask = ["ask", "raise", "funding", "investment", "seeking"]

        def check_and_suggest(keywords: List[str], feedback_msg: str, suggestion_msg: str):
            if not any(k in pitch_lower for k in keywords):
                feedback_list.append(feedback_msg)
                suggestions.append(suggestion_msg)

        check_and_suggest(keywords_problem, "The core problem you're solving is not explicitly clear.", "Start by clearly and concisely defining the significant problem your startup addresses.")
        check_and_suggest(keywords_solution, "Your proposed solution/product is not clearly articulated.", "Detail your solution, how it works, and its unique value proposition.")
        check_and_suggest(keywords_market, "Missing details on your market size or target customer.", "Quantify your market opportunity and describe your ideal customer segment.")
        check_and_suggest(keywords_team, "The pitch lacks information about your team's expertise or background.", "Highlight your team's relevant experience and why you are uniquely qualified to build this business.")
        check_and_suggest(keywords_traction, "Little to no mention of early traction or key metrics.", "If you have any users, revenue, or significant milestones, include them to demonstrate progress.")
        check_and_suggest(keywords_ask, "Your 'ask' (funding amount and use of funds) is not clear.", "State clearly how much capital you are raising and how you plan to use it to achieve milestones.")

        # Integrate Risk Profile Feedback
        if request.risk_profile:
            for rf in request.risk_profile.risk_factors:
                if rf.level == "high":
                    feedback_list.append(f"High risk identified in '{rf.name}' (Score: {request.risk_profile.overall_risk_score:.2f}% overall risk).")
                    suggestions.append(f"Explicitly address how you plan to mitigate the '{rf.name}' risk. For example: '{rf.mitigation_suggestion}'")
                    if rf.name.lower() in pitch_lower:
                        feedback_list.append(f"Good job mentioning '{rf.name}' in your pitch, but ensure your mitigation strategy is clear.")

        # Integrate Reputation Profile Feedback
        if request.reputation_profile:
            if request.reputation_profile.overall_sentiment_score < -0.3:
                feedback_list.append(f"Early sentiment is moderately negative (Score: {request.reputation_profile.overall_sentiment_score:.2f}).")
                suggestions.append("Consider acknowledging potential negative perceptions (if any) and articulate how you plan to build positive public perception.")
            elif request.reputation_profile.overall_sentiment_score > 0.3:
                feedback_list.append(f"Early sentiment is positive (Score: {request.reputation_profile.overall_sentiment_score:.2f}).")
                suggestions.append("Emphasize aspects that contribute to positive sentiment (e.g., 'innovative' or 'growth' if identified as themes).")

        # Integrate Investor Match Results Feedback
        if request.investor_match_results and request.investor_match_results.matched_investors:
            top_investor_match = request.investor_match_results.matched_investors[0]
            feedback_list.append(f"Your top investor match is '{top_investor_match.investor.name}' with a score of {top_investor_match.match_score:.2f}%.")
            if top_investor_match.gaps:
                feedback_list.append("Identify specific gaps that might deter investors:")
                suggestions.append(f"For investors like '{top_investor_match.investor.name}', consider refining your pitch to address these gaps: {'; '.join(top_investor_match.gaps)}.")
            if top_investor_match.investor.feedback_focus:
                suggestions.append(f"For investors like '{top_investor_match.investor.name}', they often focus on: {', '.join(top_investor_match.investor.feedback_focus)}. Tailor your pitch to emphasize these areas.")


        if not feedback_list: # If no specific issues found
            feedback_list.append("Your pitch seems to cover essential elements well!")
            suggestions.append("Focus on refining your delivery, storytelling, and compelling call to action. Practice makes perfect!")

        return PitchFeedbackResponse(
            startup_name=request.startup_name,
            feedback=feedback_list,
            suggestions_for_improvement=suggestions
        )