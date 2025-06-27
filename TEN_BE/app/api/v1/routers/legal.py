from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import LegalAssistanceInput, LegalAssistanceOutput
from app.services.legal_advisor import LegalAdvisorService
from app.core.dependencies import get_legal_advisor_service

router = APIRouter()

@router.post(
    "/legal-assistance",
    response_model=LegalAssistanceOutput,
    status_code=status.HTTP_200_OK,
    summary="Provides legal guidance for startups",
    description="Analyzes startup profile to recommend essential legal documents, industry-specific licenses/certifications, and key legal risks with prevention strategies."
)
async def get_legal_assistance_route(
    input_data: LegalAssistanceInput,
    legal_advisor_service: LegalAdvisorService = Depends(get_legal_advisor_service)
):
    try:
        result = await legal_advisor_service.get_legal_assistance(input_data)
        return result
    except Exception as e:
        print(f"Error in get_legal_assistance_route: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during legal assistance generation: {e}"
        )