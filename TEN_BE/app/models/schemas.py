from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any

class RiskInput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup.")
    industry: str = Field(..., description="Primary industry of the startup (e.g., 'AI', 'HealthTech').")
    market_size_usd: int = Field(..., gt=0, description="Estimated total addressable market (TAM) in USD.")
    founder_experience_years: int = Field(..., ge=0, description="Years of relevant experience of the primary founder/CEO.")
    initial_funding_needed_usd: int = Field(..., gt=0, description="Initial capital sought by the startup in USD.")

class RiskFactor(BaseModel):
    name: str = Field(..., description="Name of the risk factor (e.g., 'Market Size', 'Team Experience').")
    level: str = Field(..., description="Severity of the risk ('low', 'medium', 'high').")
    mitigation_suggestion: str = Field(..., description="Actionable suggestion to mitigate this specific risk.")

class RiskOutput(BaseModel):
    startup_name: str = Field(..., description="Name of the analyzed startup.")
    overall_risk_score: float = Field(..., ge=0, le=100, description="An overall risk score for the startup (0-100, higher is riskier).")
    risk_factors: List[RiskFactor] = Field(..., description="Detailed breakdown of identified risk factors.")
    recommendations: List[str] = Field(..., description="General recommendations based on the overall risk profile.")

class ReputationInput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup.")
    founder_twitter_handle: Optional[str] = Field(None, description="Optional Twitter handle of a key founder (e.g., 'elonmusk').")
    initial_pitch_text: str = Field(..., min_length=50, description="The initial pitch summary or description of the startup/idea. This will be the primary source for sentiment analysis.")

class ReputationOutput(BaseModel):
    startup_name: str = Field(..., description="Name of the analyzed startup.")
    overall_sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="A compound sentiment score (-1.0 to 1.0, where 1.0 is most positive).")
    positive_themes: List[str] = Field(..., description="Keywords or themes associated with positive sentiment.")
    negative_themes: List[str] = Field(..., description="Keywords or themes associated with negative sentiment.")
    neutral_themes: List[str] = Field(..., description="Keywords or themes associated with neutral or mixed sentiment.")
    actionable_insights: List[str] = Field(..., description="Suggestions for managing or leveraging the identified sentiment.")
    overall_reputation_review: str = Field(..., description="A concise overall qualitative review of the startup's/person's reputation.")

class InvestorProfile(BaseModel):
    id: str = Field(..., description="Unique identifier for the investor (can be a hash of their link).")
    name: str = Field(..., description="Name of the investor or firm (e.g., 'Sequoia Capital', 'Naval Ravikant').")
    link: Optional[HttpUrl] = Field(None, description="Direct website/profile link for the investor/firm.")
    risk_tolerance: str = Field(..., description="Investor's typical risk tolerance ('low', 'medium', 'high').")
    preferred_industries: List[str] = Field(..., description="Industries the investor typically focuses on.")
    min_investment_usd: int = Field(..., description="Minimum investment amount in USD.")
    max_investment_usd: int = Field(..., description="Maximum investment amount in USD.")
    feedback_focus: List[str] = Field(..., description="Key areas the investor typically provides feedback on or prioritizes.")

class MatchDetail(BaseModel):
    investor: InvestorProfile = Field(..., description="The matched investor's profile.")
    match_score: float = Field(..., ge=0, le=100, description="A score indicating the strength of the match (0-100%).")
    match_reasons: List[str] = Field(..., description="Reasons why this investor is a good match.")
    gaps: List[str] = Field(..., description="Areas where the startup might not perfectly align with the investor's preferences.")

class InvestorMatchInput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup.")
    industry: str = Field(..., description="Primary industry of the startup (must match one of the investor's preferred industries for a strong match).")
    funding_sought_usd: int = Field(..., gt=0, description="The amount of funding the startup is currently seeking in USD.")
    risk_profile: RiskOutput = Field(..., description="The full risk assessment output for the startup.")
    reputation_profile: ReputationOutput = Field(..., description="The full reputation analysis output for the startup.")

# InvestorMatchOutput MUST be defined before PitchFeedbackRequest
class InvestorMatchOutput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup for which matches were found.")
    matched_investors: List[MatchDetail] = Field(..., description="A list of potential investor matches, ordered by match score.")

class PitchFeedbackRequest(BaseModel):
    startup_name: str = Field(..., description="Name of the startup.")
    pitch_text: str = Field(..., min_length=100, description="The full text of the startup's pitch (e.g., executive summary, elevator pitch).")
    risk_profile: Optional[RiskOutput] = Field(None, description="Optional: The risk assessment output for more tailored feedback.")
    reputation_profile: Optional[ReputationOutput] = Field(None, description="Optional: The reputation analysis output for more tailored feedback.")
    investor_match_results: Optional[InvestorMatchOutput] = Field(None, description="Optional: The investor matching results to tailor feedback towards specific investor types.")

class PitchFeedbackResponse(BaseModel):
    startup_name: str = Field(..., description="Name of the startup that received feedback.")
    feedback: List[str] = Field(..., description="General feedback points on the pitch.")
    suggestions_for_improvement: List[str] = Field(..., description="Actionable suggestions to improve the pitch.")

# --- NEW: Legal Assistance Models ---

class LegalAssistanceInput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup.")
    industry: str = Field(..., description="Primary industry of the startup (e.g., 'Food Tech', 'SaaS', 'FinTech').")
    business_model_summary: str = Field(..., min_length=50, description="A brief summary of what your business does and how it operates (e.g., 'develops mobile app for food delivery', 'sells organic skincare products online').")
    funding_stage: str = Field(..., description="Current funding stage (e.g., 'ideation', 'pre-seed', 'seed', 'Series A', 'bootstrapped').")
    num_founders: int = Field(..., ge=1, description="Number of co-founders.")
    num_employees: int = Field(..., ge=0, description="Current number of employees (excluding founders).")
    handles_personal_data: bool = Field(..., description="Does your business collect, store, or process personal data (e.g., user profiles, health info)?")
    sells_physical_products: bool = Field(..., description="Does your business sell physical products (vs. purely digital services)?")

class LegalDocument(BaseModel):
    name: str = Field(..., description="Name of the legal document (e.g., 'Founder's Agreement', 'NDA').")
    description: str = Field(..., description="Brief description of the document's purpose.")
    relevance_reason: str = Field(..., description="Why this document is relevant for the startup.")

class LicenseCertification(BaseModel):
    name: str = Field(..., description="Name of the license/certification (e.g., 'Food Handler's Permit').")
    description: str = Field(..., description="Brief description of what it entails.")
    relevance_reason: str = Field(..., description="Why this is relevant based on industry/business model.")

class LegalRisk(BaseModel):
    name: str = Field(..., description="Name of the legal risk (e.g., 'IP Infringement', 'Data Breach').")
    description: str = Field(..., description="Description of the risk.")
    prevention_strategy: str = Field(..., description="Actionable steps to prevent or mitigate this risk.")

class LegalAssistanceOutput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup.")
    essential_documents: List[LegalDocument] = Field(..., description="List of essential legal documents recommended.")
    industry_licenses_certs: List[LicenseCertification] = Field(..., description="List of industry-specific licenses or certifications recommended.")
    key_legal_risks: List[LegalRisk] = Field(..., description="List of key legal risks and their prevention strategies.")
    general_legal_advice: List[str] = Field(..., description="General legal recommendations for the startup.")