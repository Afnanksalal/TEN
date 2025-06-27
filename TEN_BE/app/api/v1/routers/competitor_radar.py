from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import CompetitorRadarInput, CompetitorRadarOutput
from app.services.competitor_radar import CompetitorRadarService
from app.core.dependencies import get_competitor_radar_service

router = APIRouter()

@router.post(
    "/competitor-radar",
    response_model=CompetitorRadarOutput,
    status_code=status.HTTP_200_OK,
    summary="Track emerging competitors and market trends",
    description="Uses AI and web scraping (SerpAPI) to identify and track competitors, showing their funding, press, and hiring surges, along with general market trends."
)
async def competitor_radar_route(
    input_data: CompetitorRadarInput,
    radar_service: CompetitorRadarService = Depends(get_competitor_radar_service)
):
    try:
        result = await radar_service.track_competitors(input_data)
        return result
    except Exception as e:
        print(f"Error in competitor_radar_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during competitor tracking: {e}"
        )