from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import ExitStrategyExplorerInput, ExitStrategyExplorerOutput
from app.services.exit_strategy_explorer import ExitStrategyExplorerService
from app.core.dependencies import get_exit_strategy_explorer_service

router = APIRouter()

@router.post(
    "/exit-strategy-explorer",
    response_model=ExitStrategyExplorerOutput,
    status_code=status.HTTP_200_OK,
    summary="Explore potential exit strategies for your startup",
    description="Provides AI-driven insights into relevant exit strategies, common acquirer types, key metrics for attractiveness, and actionable steps to improve readiness."
)
async def exit_strategy_explorer_route(
    input_data: ExitStrategyExplorerInput,
    explorer_service: ExitStrategyExplorerService = Depends(get_exit_strategy_explorer_service)
):
    try:
        result = await explorer_service.explore_exit_strategies(input_data)
        return result
    except Exception as e:
        print(f"Error in exit_strategy_explorer_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during exit strategy exploration: {e}"
        )