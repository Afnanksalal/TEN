from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import TractionEstimatorInput, TractionEstimatorOutput
from app.services.traction_estimator import TractionEstimatorService
from app.core.dependencies import get_traction_estimator_service

router = APIRouter()

@router.post(
    "/traction-estimator",
    response_model=TractionEstimatorOutput,
    status_code=status.HTTP_200_OK,
    summary="Estimate growth traction and get benchmarks",
    description="Analyzes your startup's metrics, benchmarks them against industry averages, and provides an AI-generated growth health score and actionable insights."
)
async def traction_estimator_route(
    input_data: TractionEstimatorInput,
    estimator_service: TractionEstimatorService = Depends(get_traction_estimator_service)
):
    try:
        result = await estimator_service.estimate_traction(input_data)
        return result
    except Exception as e:
        print(f"Error in traction_estimator_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during traction estimation: {e}"
        )