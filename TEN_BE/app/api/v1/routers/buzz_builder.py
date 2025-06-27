from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import BuzzBuilderInput, BuzzBuilderOutput
from app.services.buzz_builder import BuzzBuilderService
from app.core.dependencies import get_buzz_builder_service

router = APIRouter()

@router.post(
    "/buzz-builder",
    response_model=BuzzBuilderOutput,
    status_code=status.HTTP_200_OK,
    summary="Generate social media and blog content ideas",
    description="Uses AI to suggest tweet threads, LinkedIn posts, and blog topics tailored to your startup's narrative and recent milestones."
)
async def buzz_builder_route(
    input_data: BuzzBuilderInput,
    builder_service: BuzzBuilderService = Depends(get_buzz_builder_service)
):
    try:
        result = await builder_service.generate_buzz(input_data)
        return result
    except Exception as e:
        print(f"Error in buzz_builder_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during buzz generation: {e}"
        )