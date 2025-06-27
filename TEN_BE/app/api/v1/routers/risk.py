from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import RiskInput, RiskOutput
from app.services.risk_analyzer import RiskAnalyzerService
from app.core.dependencies import get_risk_analyzer_service

# Initialize FastAPI APIRouter
router = APIRouter()

@router.post(
    "/analyze-risk",
    response_model=RiskOutput,
    status_code=status.HTTP_200_OK,
    summary="Analyzes startup risk profile",
    description="Evaluates a startup's profile (market, founder experience, funding needs) to generate a risk assessment. Returns overall risk score, specific risk factors, and mitigation recommendations."
)
async def analyze_risk_route(
    input_data: RiskInput,
    analyzer_service: RiskAnalyzerService = Depends(get_risk_analyzer_service)
):
    """
    **Request Body (RiskInput):**
    - `startup_name`: (string) Name of the startup.
    - `industry`: (string) Primary industry (e.g., 'AI', 'HealthTech').
    - `market_size_usd`: (integer) Estimated total addressable market in USD.
    - `founder_experience_years`: (integer) Years of relevant experience.
    - `initial_funding_needed_usd`: (integer) Initial capital sought.

    **Response (RiskOutput):**
    - `startup_name`: (string)
    - `overall_risk_score`: (float) 0-100, higher is riskier.
    - `risk_factors`: (array of objects) Specific risks (name, level, suggestion).
    - `recommendations`: (array of strings) General advice.
    """
    try:
        result = await analyzer_service.analyze_risk(input_data)
        return result
    except Exception as e:
        # Log the error for debugging purposes in a real application
        print(f"Error in analyze_risk_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during risk analysis: {e}"
        )