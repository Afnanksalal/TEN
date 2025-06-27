from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any

# --- 1. Risk Assessment Models ---

class RiskInput(BaseModel):
    """
    Input schema for the risk analysis service.
    """
    startup_name: str = Field(..., description="Name of the startup.")
    industry: str = Field(..., description="Primary industry of the startup (e.g., 'AI', 'HealthTech').")
    market_size_usd: int = Field(..., gt=0, description="Estimated total addressable market (TAM) in USD.")
    founder_experience_years: int = Field(..., ge=0, description="Years of relevant experience of the primary founder/CEO.")
    initial_funding_needed_usd: int = Field(..., gt=0, description="Initial capital sought by the startup in USD.")

class RiskFactor(BaseModel):
    """
    Represents a specific risk factor identified for the startup.
    """
    name: str = Field(..., description="Name of the risk factor (e.g., 'Market Size', 'Team Experience').")
    level: str = Field(..., description="Severity of the risk ('low', 'medium', 'high').")
    mitigation_suggestion: str = Field(..., description="Actionable suggestion to mitigate this specific risk.")

class RiskOutput(BaseModel):
    """
    Output schema for the risk analysis service.
    """
    startup_name: str = Field(..., description="Name of the analyzed startup.")
    overall_risk_score: float = Field(..., ge=0, le=100, description="An overall risk score for the startup (0-100, higher is riskier).")
    risk_factors: List[RiskFactor] = Field(..., description="Detailed breakdown of identified risk factors.")
    recommendations: List[str] = Field(..., description="General recommendations based on the overall risk profile.")


# --- 2. Reputation Analysis Models ---

class ReputationInput(BaseModel):
    """
    Input schema for the reputation scanning service.
    For hackathon, focus on initial pitch text as source.
    """
    startup_name: str = Field(..., description="Name of the startup.")
    # Optional fields for more advanced (future) scanning
    founder_linkedin_url: Optional[HttpUrl] = Field(None, description="Optional LinkedIn URL of a key founder.")
    founder_twitter_handle: Optional[str] = Field(None, description="Optional Twitter handle of a key founder (e.g., 'elonmusk').")
    initial_pitch_text: str = Field(..., min_length=50, description="The initial pitch summary or description of the startup/idea. This will be the primary source for sentiment analysis.")

class ReputationOutput(BaseModel):
    """
    Output schema for the reputation scanning service.
    """
    startup_name: str = Field(..., description="Name of the analyzed startup.")
    overall_sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="A compound sentiment score (-1.0 to 1.0, where 1.0 is most positive).")
    positive_themes: List[str] = Field(..., description="Keywords or themes associated with positive sentiment.")
    negative_themes: List[str] = Field(..., description="Keywords or themes associated with negative sentiment.")
    neutral_themes: List[str] = Field(..., description="Keywords or themes associated with neutral or mixed sentiment.")
    actionable_insights: List[str] = Field(..., description="Suggestions for managing or leveraging the identified sentiment.")


# --- 3. Investor Matching & Pitch Feedback Models ---

class InvestorProfile(BaseModel):
    """
    Represents a simplified investor profile (from app/data/investor_profiles.json).
    """
    id: str = Field(..., description="Unique ID for the investor profile.")
    name: str = Field(..., description="Name of the investor or fund.")
    risk_tolerance: str = Field(..., description="Investor's typical risk tolerance ('low', 'medium', 'high').")
    preferred_industries: List[str] = Field(..., description="Industries the investor typically focuses on.")
    min_investment_usd: int = Field(..., description="Minimum investment amount in USD.")
    max_investment_usd: int = Field(..., description="Maximum investment amount in USD.")
    feedback_focus: List[str] = Field(..., description="Key areas the investor typically provides feedback on or prioritizes (e.g., 'team', 'traction').")

class MatchDetail(BaseModel):
    """
    Details of a single investor match for a startup.
    """
    investor: InvestorProfile = Field(..., description="The matched investor's profile.")
    match_score: float = Field(..., ge=0, le=100, description="A score indicating the strength of the match (0-100%).")
    match_reasons: List[str] = Field(..., description="Reasons why this investor is a good match.")
    gaps: List[str] = Field(..., description="Areas where the startup might not perfectly align with the investor's preferences.")

class InvestorMatchInput(BaseModel):
    """
    Input schema for the investor matching service.
    Combines startup details with its generated risk and reputation profiles.
    """
    startup_name: str = Field(..., description="Name of the startup.")
    industry: str = Field(..., description="Primary industry of the startup (must match one of the investor's preferred industries for a strong match).")
    funding_sought_usd: int = Field(..., gt=0, description="The amount of funding the startup is currently seeking in USD.")
    risk_profile: RiskOutput = Field(..., description="The full risk assessment output for the startup.")
    reputation_profile: ReputationOutput = Field(..., description="The full reputation analysis output for the startup.")

class InvestorMatchOutput(BaseModel):
    """
    Output schema for the investor matching service.
    """
    startup_name: str = Field(..., description="Name of the startup for which matches were found.")
    matched_investors: List[MatchDetail] = Field(..., description="A list of potential investor matches, ordered by match score.")

class PitchFeedbackRequest(BaseModel):
    """
    Input schema for the pitch feedback generation service.
    Allows passing previously generated analysis results for more targeted feedback.
    """
    startup_name: str = Field(..., description="Name of the startup.")
    pitch_text: str = Field(..., min_length=100, description="The full text of the startup's pitch (e.g., executive summary, elevator pitch).")
    risk_profile: Optional[RiskOutput] = Field(None, description="Optional: The risk assessment output for more tailored feedback.")
    reputation_profile: Optional[ReputationOutput] = Field(None, description="Optional: The reputation analysis output for more tailored feedback.")
    investor_match_results: Optional[InvestorMatchOutput] = Field(None, description="Optional: The investor matching results to tailor feedback towards specific investor types.")

class PitchFeedbackResponse(BaseModel):
    """
    Output schema for the pitch feedback generation service.
    """
    startup_name: str = Field(..., description="Name of the startup that received feedback.")
    feedback: List[str] = Field(..., description="General feedback points on the pitch.")
    suggestions_for_improvement: List[str] = Field(..., description="Actionable suggestions to improve the pitch.")