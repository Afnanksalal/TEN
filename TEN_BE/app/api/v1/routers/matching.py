from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import (
    InvestorMatchInput, InvestorMatchOutput,
    PitchFeedbackRequest, PitchFeedbackResponse
)
from app.services.investor_matcher import InvestorMatcherService
from app.services.pitch_feedback_generator import PitchFeedbackGeneratorService
from app.core.dependencies import get_investor_matcher_service, get_pitch_feedback_generator_service

# Initialize FastAPI APIRouter
router = APIRouter()

@router.post(
    "/match-investors",
    response_model=InvestorMatchOutput,
    status_code=status.HTTP_200_OK,
    summary="Finds suitable investors for a startup",
    description="Matches a startup's profile (industry, funding, risk, and early sentiment) with simulated investor preferences. Returns a list of potential investor matches with detailed reasons and identified gaps."
)
async def match_investors_route(
    input_data: InvestorMatchInput,
    matcher_service: InvestorMatcherService = Depends(get_investor_matcher_service)
):
    """
    **Request Body (InvestorMatchInput):**
    - `startup_name`: (string)
    - `industry`: (string)
    - `funding_sought_usd`: (integer)
    - `risk_profile`: (object) The full `RiskOutput` object from /analyze-risk.
    - `reputation_profile`: (object) The full `ReputationOutput` object from /scan-reputation.

    **Response (InvestorMatchOutput):**
    - `startup_name`: (string)
    - `matched_investors`: (array of objects) Each object includes:
        - `investor`: (object) Detailed investor profile.
        - `match_score`: (float) 0-100% score.
        - `match_reasons`: (array of strings) Why it's a good match.
        - `gaps`: (array of strings) Areas of misalignment.
    """
    try:
        result = await matcher_service.match_investors(input_data)
        return result
    except Exception as e:
        print(f"Error in match_investors_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during investor matching: {e}"
        )

@router.post(
    "/pitch-feedback",
    response_model=PitchFeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Generates feedback for a startup pitch",
    description="Provides constructive feedback and actionable suggestions for improving a startup's pitch. Can be enhanced with previous risk, reputation, and investor matching results for more targeted advice."
)
async def get_pitch_feedback_route(
    request: PitchFeedbackRequest,
    feedback_service: PitchFeedbackGeneratorService = Depends(get_pitch_feedback_generator_service)
):
    """
    **Request Body (PitchFeedbackRequest):**
    - `startup_name`: (string)
    - `pitch_text`: (string) The full text of the pitch.
    - `risk_profile`: (object, optional) Include `RiskOutput` for tailored feedback.
    - `reputation_profile`: (object, optional) Include `ReputationOutput` for tailored feedback.
    - `investor_match_results`: (object, optional) Include `InvestorMatchOutput` for investor-specific advice.

    **Response (PitchFeedbackResponse):**
    - `startup_name`: (string)
    - `feedback`: (array of strings) General observations.
    - `suggestions_for_improvement`: (array of strings) Concrete actionable steps.
    """
    try:
        result = await feedback_service.generate_feedback(request)
        return result
    except Exception as e:
        print(f"Error in get_pitch_feedback_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during pitch feedback generation: {e}"
        )