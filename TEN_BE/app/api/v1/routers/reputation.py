from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import ReputationInput, ReputationOutput
from app.services.reputation_scanner import ReputationScannerService
from app.core.dependencies import get_reputation_scanner_service

router = APIRouter()

@router.post(
    "/scan-reputation",
    response_model=ReputationOutput,
    status_code=status.HTTP_200_OK,
    summary="Scans early market/founder sentiment",
    description="Analyzes provided text (e.g., initial pitch) and mock social media presence to gauge early sentiment and identify key themes (positive, negative, neutral). Returns actionable insights for managing public perception."
)
async def scan_reputation_route(
    input_data: ReputationInput,
    scanner_service: ReputationScannerService = Depends(get_reputation_scanner_service)
):
    """
    **Request Body (ReputationInput):**
    - `startup_name`: (string) Name of the startup.
    - `founder_linkedin_url`: (string, optional) LinkedIn profile URL.
    - `founder_twitter_handle`: (string, optional) Twitter handle.
    - `initial_pitch_text`: (string) The core text for sentiment analysis.

    **Response (ReputationOutput):**
    - `startup_name`: (string)
    - `overall_sentiment_score`: (float) -1.0 to 1.0 (compound score).
    - `positive_themes`: (array of strings)
    - `negative_themes`: (array of strings)
    - `neutral_themes`: (array of strings)
    - `actionable_insights`: (array of strings) Suggestions for leveraging/managing sentiment.
    """
    try:
        result = await scanner_service.scan_reputation(input_data)
        return result
    except Exception as e:
        print(f"Error in scan_reputation_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during reputation scanning: {e}"
        )
