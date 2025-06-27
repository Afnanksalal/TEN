from fastapi import Depends
from typing import Awaitable
import redis.asyncio as redis
import google.generativeai as genai

# Import all service classes
from app.core.redis import get_redis_client
from app.core.gemini_client import get_gemini_model
from app.services.risk_analyzer import RiskAnalyzerService
from app.services.reputation_scanner import ReputationScannerService
from app.services.investor_matcher import InvestorMatcherService
from app.services.pitch_feedback_generator import PitchFeedbackGeneratorService
from app.services.competitor_radar import CompetitorRadarService
from app.services.traction_estimator import TractionEstimatorService
from app.services.buzz_builder import BuzzBuilderService
from app.services.legal_advisor import LegalAdvisorService # Correct import, using LegalAdvisorService


async def get_redis_dependency() -> redis.Redis:
    return await get_redis_client()

async def get_risk_analyzer_service(
    redis_client: redis.Redis = Depends(get_redis_dependency),
    gemini_model: genai.GenerativeModel = Depends(get_gemini_model)
) -> RiskAnalyzerService:
    return RiskAnalyzerService(redis_client=redis_client, gemini_model=gemini_model)

async def get_reputation_scanner_service(
    redis_client: redis.Redis = Depends(get_redis_dependency),
    gemini_model: genai.GenerativeModel = Depends(get_gemini_model)
) -> ReputationScannerService:
    return ReputationScannerService(redis_client=redis_client, gemini_model=gemini_model)

async def get_investor_matcher_service(
    redis_client: redis.Redis = Depends(get_redis_dependency),
    gemini_model: genai.GenerativeModel = Depends(get_gemini_model)
) -> InvestorMatcherService:
    return InvestorMatcherService(redis_client=redis_client, gemini_model=gemini_model)

async def get_pitch_feedback_generator_service(
    redis_client: redis.Redis = Depends(get_redis_dependency),
    gemini_model: genai.GenerativeModel = Depends(get_gemini_model)
) -> PitchFeedbackGeneratorService:
    return PitchFeedbackGeneratorService(redis_client=redis_client, gemini_model=gemini_model)

async def get_competitor_radar_service(
    redis_client: redis.Redis = Depends(get_redis_dependency),
    gemini_model: genai.GenerativeModel = Depends(get_gemini_model)
) -> CompetitorRadarService:
    return CompetitorRadarService(redis_client=redis_client, gemini_model=gemini_model)

async def get_traction_estimator_service(
    redis_client: redis.Redis = Depends(get_redis_dependency),
    gemini_model: genai.GenerativeModel = Depends(get_gemini_model)
) -> TractionEstimatorService:
    return TractionEstimatorService(redis_client=redis_client, gemini_model=gemini_model)

async def get_buzz_builder_service(
    redis_client: redis.Redis = Depends(get_redis_dependency),
    gemini_model: genai.GenerativeModel = Depends(get_gemini_model)
) -> BuzzBuilderService:
    return BuzzBuilderService(redis_client=redis_client, gemini_model=gemini_model)

async def get_legal_advisor_service(
    redis_client: redis.Redis = Depends(get_redis_dependency),
    gemini_model: genai.GenerativeModel = Depends(get_gemini_model)
) -> LegalAdvisorService: 
    return LegalAdvisorService(redis_client=redis_client, gemini_model=gemini_model)