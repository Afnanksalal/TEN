from fastapi import Depends
from typing import Awaitable
from typing import Optional

import redis.asyncio as redis
from app.core.redis import get_redis_client
from app.services.risk_analyzer import RiskAnalyzerService
from app.services.reputation_scanner import ReputationScannerService
from app.services.investor_matcher import InvestorMatcherService
from app.services.pitch_feedback_generator import PitchFeedbackGeneratorService

# --- Redis Dependency ---
async def get_redis_dependency():
    """
    Dependency that provides the Redis client instance.
    """
    return await get_redis_client()

# --- Service Dependencies ---
# Each service depends on the Redis client, so we pass it in using Depends()

async def get_risk_analyzer_service(
    redis_client: Awaitable[redis.Redis] = Depends(get_redis_dependency)
) -> RiskAnalyzerService:
    """
    Dependency that provides an instance of RiskAnalyzerService.
    """
    return RiskAnalyzerService(redis_client=await redis_client)

async def get_reputation_scanner_service(
    redis_client: Awaitable[redis.Redis] = Depends(get_redis_dependency)
) -> ReputationScannerService:
    """
    Dependency that provides an instance of ReputationScannerService.
    """
    return ReputationScannerService(redis_client=await redis_client)

async def get_investor_matcher_service(
    redis_client: Awaitable[redis.Redis] = Depends(get_redis_dependency)
) -> InvestorMatcherService:
    """
    Dependency that provides an instance of InvestorMatcherService.
    """
    return InvestorMatcherService(redis_client=await redis_client)

async def get_pitch_feedback_generator_service(
    redis_client: Awaitable[redis.Redis] = Depends(get_redis_dependency)
) -> PitchFeedbackGeneratorService:
    """
    Dependency that provides an instance of PitchFeedbackGeneratorService.
    """
    return PitchFeedbackGeneratorService(redis_client=await redis_client)