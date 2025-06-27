from pydantic import BaseModel, HttpUrl, Field, validator
from typing import List, Optional, Dict, Any

# --- 1. Risk Assessment Models ---

class RiskInput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup.")
    industry: str = Field(..., description="Primary industry of the startup (e.g., 'AI', 'HealthTech').")
    specific_product_service: str = Field(..., min_length=10, description="A brief description of the specific product or service the startup offers (e.g., 'AI-powered diagnostic tool for rare diseases', 'IoT sensors for smart home automation', 'SaaS platform for small business accounting').")
    market_size_usd: int = Field(..., gt=0, description="Estimated total addressable market (TAM) in USD.")
    founder_experience_years: int = Field(..., ge=0, description="Years of relevant experience of the primary founder/CEO.")
    initial_funding_needed_usd: int = Field(..., gt=0, description="Initial capital sought by the startup in USD.")

    has_mvp: Optional[bool] = Field(None, description="Does the startup currently have a Minimum Viable Product (MVP) developed?")
    mvp_stage_description: Optional[str] = Field(None, description="If MVP exists, briefly describe its current functionality and user engagement (e.g., 'basic functionality, 50 beta users', 'core features, 10 paying customers').", min_length=10)
    
    intellectual_property_status: Optional[str] = Field(None, description="Status of intellectual property (e.g., 'patent filed', 'trademark pending', 'trade secrets', 'none').")
    
    regulatory_environment: Optional[str] = Field(None, description="Describes the typical regulatory hurdles in the startup's domain (e.g., 'heavily regulated (e.g., FDA)', 'moderately regulated (e.g., data privacy)', 'lightly regulated').")
    
    burn_rate_usd_per_month: Optional[int] = Field(None, ge=0, description="Estimated monthly burn rate in USD.")
    runway_months: Optional[int] = Field(None, ge=0, description="Estimated months of runway with current funds.")

    num_direct_competitors: Optional[int] = Field(None, ge=0, description="Estimated number of direct competitors.")
    competitive_advantage: Optional[str] = Field(None, description="Briefly describe the startup's main competitive advantage (e.g., 'proprietary tech', 'first-mover', 'strong network effects').", min_length=10)

    @validator('mvp_stage_description', pre=True, always=True)
    def check_mvp_description_if_has_mvp(cls, v, values):
        if values.get('has_mvp') is True and (v is None or not v.strip()):
            raise ValueError('mvp_stage_description must be provided if has_mvp is True')
        return v

class RiskFactor(BaseModel):
    name: str = Field(..., description="Name of the risk factor (e.g., 'Market Size', 'Team Experience').")
    level: str = Field(..., description="Severity of the risk ('low', 'medium', 'high').")
    mitigation_suggestion: str = Field(..., description="Actionable suggestion to mitigate this specific risk.")

class RiskOutput(BaseModel):
    startup_name: str = Field(..., description="Name of the analyzed startup.")
    overall_risk_score: float = Field(..., ge=0, le=100, description="An overall risk score for the startup (0-100, higher is riskier).")
    risk_factors: List[RiskFactor] = Field(..., description="Detailed breakdown of identified risk factors.")
    recommendations: List[str] = Field(..., description="General recommendations based on the overall risk profile.")


# --- 2. Reputation Analysis Models ---

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

# --- 4. Competitor Radar Models ---
class CompetitorRadarInput(BaseModel):
    startup_name: str = Field(..., description="Your startup's name.")
    your_industry: str = Field(..., description="Your primary industry for context.")
    # NEW FIELD
    your_product_service_description: str = Field(..., min_length=20, description="A brief description of your startup's core product or service for better competitor identification.")
    
class CompetitorInfo(BaseModel):
    name: str = Field(..., description="Competitor's name.")
    website: Optional[HttpUrl] = Field(None, description="Competitor's website URL.")
    product_description: Optional[str] = Field(None, description="AI-extracted brief description of competitor's product/service.") # NEW FIELD
    value_proposition: Optional[str] = Field(None, description="AI-extracted key value proposition of the competitor.") # NEW FIELD
    target_market: Optional[str] = Field(None, description="AI-extracted target market of the competitor.") # NEW FIELD
    funding_rounds: List[str] = Field(..., description="Recent funding rounds detected (e.g., 'Series A: $5M from XYZ Ventures').")
    press_mentions_summary: List[str] = Field(..., description="Key press mentions or recent news headlines/summaries.")
    hiring_surge_indication: str = Field(..., description="AI assessment of hiring activity (e.g., 'High', 'Medium', 'Low', 'No indication').")
    overall_summary: str = Field(..., description="AI-generated brief summary of the competitor's recent activity.")

class CompetitorRadarOutput(BaseModel):
    startup_name: str = Field(..., description="Your startup's name as input.")
    tracked_competitors: List[CompetitorInfo] = Field(..., description="List of tracked competitors with relevant intelligence.")
    general_market_trends: List[str] = Field(..., description="AI-generated general market trends based on competitor activity.")


# --- 5. Traction Estimator Models ---
class TractionEstimatorInput(BaseModel):
    startup_name: str = Field(..., description="Your startup's name.")
    your_industry: str = Field(..., description="Your primary industry (e.g., 'SaaS', 'eCommerce').")
    monthly_active_users: Optional[int] = Field(None, ge=0, description="Current Monthly Active Users (MAU).")
    monthly_recurring_revenue_usd: Optional[float] = Field(None, ge=0.0, description="Current Monthly Recurring Revenue (MRR) in USD.")
    customer_acquisition_cost_usd: Optional[float] = Field(None, ge=0.0, description="Customer Acquisition Cost (CAC) in USD.")
    customer_lifetime_value_usd: Optional[float] = Field(None, ge=0.0, description="Customer Lifetime Value (LTV) in USD.")
    churn_rate_percent: Optional[float] = Field(None, ge=0.0, le=100.0, description="Monthly churn rate in percentage (0-100).")
    conversion_rate_percent: Optional[float] = Field(None, ge=0.0, le=100.0, description="Conversion rate from lead to customer in percentage.")

class TractionBenchmark(BaseModel):
    metric: str = Field(..., description="Metric being benchmarked.")
    your_value: Optional[float] = Field(None, description="Your startup's value for this metric.")
    industry_average: Optional[float] = Field(None, description="Simulated industry average for this metric.")
    comparison: str = Field(..., description="AI comparison of your value vs. industry average (e.g., 'Above average', 'Below average').")

class TractionEstimatorOutput(BaseModel):
    startup_name: str = Field(..., description="Your startup's name as input.")
    growth_health_score: float = Field(..., ge=0, le=100, description="AI-generated score (0-100) indicating the overall health of your growth metrics.")
    benchmarks: List[TractionBenchmark] = Field(..., description="Comparison of your metrics against simulated industry benchmarks.")
    ai_insights: List[str] = Field(..., description="AI-generated insights and tips for improving traction.")

# --- 6. Buzz Builder Models ---
class BuzzBuilderInput(BaseModel):
    startup_name: str = Field(..., description="Your startup's name.")
    your_industry: str = Field(..., description="Your primary industry for context.")
    current_milestones: List[str] = Field(..., description="Recent achievements or updates (e.g., 'Launched MVP', 'Secured 1000 users', 'Raised seed round').")
    key_message: str = Field(..., description="The main message or narrative you want to convey.")
    target_audience: str = Field(..., description="Who you are trying to reach (e.g., 'early adopters', 'investors', 'potential hires').")

class SocialPostSuggestion(BaseModel):
    platform: str = Field(..., description="Suggested platform (e.g., 'Twitter Thread', 'LinkedIn Post', 'Blog Post Idea').")
    title: str = Field(..., description="A compelling title or thread starter.")
    content_points: List[str] = Field(..., description="Key bullet points or paragraphs for the content.")
    hashtags: List[str] = Field(..., description="Relevant hashtags.")
    call_to_action: str = Field(..., description="Suggested call to action.")

class BuzzBuilderOutput(BaseModel):
    startup_name: str = Field(..., description="Your startup's name as input.")
    suggestions: List[SocialPostSuggestion] = Field(..., description="List of generated content suggestions for various platforms.")
    ai_tips: List[str] = Field(..., description="AI-generated tips for maximizing buzz.")


# --- 7. Legal Assistance Models ---
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
    disclaimer: str = Field(
        "This AI guidance is for informational purposes only and does not constitute legal advice. "
        "Always consult with a qualified legal professional for specific legal matters. "
        "Laws vary by jurisdiction and circumstances.",
        description="Disclaimer for legal guidance."
    )

# --- 8. Exit Strategy Explorer Models ---
class AcquirerType(BaseModel):
    type_name: str = Field(..., description="Type of acquirer (e.g., 'Strategic Buyer', 'Private Equity Firm').")

class ActionItem(BaseModel):
    item: str = Field(..., description="An actionable step the startup can take.")

class ExitStrategy(BaseModel):
    strategy_name: str = Field(..., description="Name of the exit strategy (e.g., 'Acquisition by Strategic Buyer', 'IPO').")
    description: str = Field(..., description="Brief description of the strategy.")
    common_acquirer_types: List[AcquirerType] = Field(..., description="Common types of acquirers or strategic partners.")
    attractiveness_metrics: List[str] = Field(..., description="Key metrics/characteristics that make a company attractive for this strategy.")
    action_items: List[ActionItem] = Field(..., description="Actionable steps to improve readiness for this strategy.")

class ExitStrategyExplorerInput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup.")
    industry: str = Field(..., description="Industry of the startup.")
    business_model_summary: str = Field(..., min_length=50, description="A summary of the startup's business model.")
    funding_stage: str = Field(..., description="Current funding stage (e.g., 'seed', 'Series A').")
    current_revenue_usd: Optional[float] = Field(None, ge=0.0, description="Current annual or monthly recurring revenue in USD.")
    monthly_active_users: Optional[int] = Field(None, ge=0, description="Current Monthly Active Users (MAU) for digital products.")
    competitive_landscape_summary: Optional[str] = Field(None, min_length=20, description="A brief summary of the competitive landscape and the startup's position.")
    ip_status: Optional[str] = Field(None, description="Status of intellectual property (e.g., 'Patented technology', 'Trade secrets', 'Open-source contribution').")
    unique_value_proposition: Optional[str] = Field(None, min_length=20, description="What makes the startup uniquely valuable or difficult to replicate.")
    founder_exit_goals: Optional[str] = Field(None, description="The founders' long-term goals for an exit (e.g., 'maximize valuation', 'ensure product continuity', 'quick exit').")


class ExitStrategyExplorerOutput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup analyzed.")
    relevant_exit_strategies: List[ExitStrategy] = Field(..., description="List of relevant exit strategies with details.")
    strategic_planning_tips: List[str] = Field(..., description="General AI tips for long-term strategic planning.")

# --- 9. Talent Navigator Models ---
class InterviewQuestion(BaseModel):
    question: str = Field(..., description="A specific, insightful interview question.")

class RecommendedRole(BaseModel):
    role_name: str = Field(..., description="Name of the recommended role (e.g., 'Head of Product', 'Senior Backend Engineer').")
    ideal_candidate_profile: str = Field(..., description="Description of the ideal candidate profile (key skills, experience, traits).")
    interview_questions: List[InterviewQuestion] = Field(..., description="Suggested interview questions for this role.")

class TalentTip(BaseModel):
    tip: str = Field(..., description="An AI coaching tip for team building.")

class TalentNavigatorInput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup.")
    your_industry: str = Field(..., description="Your primary industry for context.")
    funding_stage: str = Field(..., description="Current funding stage (e.g., 'pre-seed', 'seed').")
    current_team_size: int = Field(..., ge=0, description="Current number of team members.")
    key_challenge: str = Field(..., min_length=20, description="The key challenge the startup is facing that talent could help address.")

class TalentNavigatorOutput(BaseModel):
    startup_name: str = Field(..., description="Name of the startup analyzed.")
    recommended_roles: List[RecommendedRole] = Field(..., description="List of recommended roles with candidate profiles and interview questions.")
    team_building_tips: List[TalentTip] = Field(..., description="General AI coaching tips for building a strong early-stage team.")
