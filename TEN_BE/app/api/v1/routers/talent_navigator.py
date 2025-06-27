from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import TalentNavigatorInput, TalentNavigatorOutput
from app.services.talent_navigator import TalentNavigatorService
from app.core.dependencies import get_talent_navigator_service

router = APIRouter()

@router.post(
    "/talent-navigator",
    response_model=TalentNavigatorOutput,
    status_code=status.HTTP_200_OK,
    summary="Get AI guidance for team building and key hires",
    description="Provides AI-driven recommendations for key roles, ideal candidate profiles, interview questions, and tips for building a strong early-stage team."
)
async def talent_navigator_route(
    input_data: TalentNavigatorInput,
    talent_service: TalentNavigatorService = Depends(get_talent_navigator_service)
):
    try:
        result = await talent_service.get_talent_guidance(input_data)
        return result
    except Exception as e:
        print(f"Error in talent_navigator_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during talent guidance generation: {e}"
        )