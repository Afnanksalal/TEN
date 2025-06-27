from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import (
    risk,
    reputation,
    matching,
    competitor_radar,
    traction_estimator,
    buzz_builder,
    legal,
    exit_strategy_explorer,
    talent_navigator,
)
from app.core.config import settings
from app.core.redis import connect_redis, disconnect_redis, get_redis_client
from app.core.gemini_client import init_gemini_model
import uvicorn

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from app.core.security import get_api_key

GLOBAL_DEFAULT_RATE_LIMIT = Depends(RateLimiter(times=100, seconds=60))

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="An AI-powered platform to assist first-time entrepreneurs with risk assessment, reputation analysis, and investor matching.",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_redis()

    try:
        redis_client = await get_redis_client()
        await FastAPILimiter.init(redis=redis_client)
    except ConnectionError as e:
        print(f"WARNING: Could not initialize FastAPI-Limiter: {e}. Rate limiting will not be active.")
    except Exception as e:
        print(f"An unexpected error occurred during FastAPI-Limiter initialization: {e}")

    init_gemini_model()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_redis()

routers_config = [
    (risk, "/api/v1", ["Risk Assessment"]),
    (reputation, "/api/v1", ["Reputation Analysis"]),
    (matching, "/api/v1", ["Investor Matching & Pitch Feedback"]),
    (competitor_radar, "/api/v1", ["Competitor Radar"]),
    (traction_estimator, "/api/v1", ["Traction Estimator"]),
    (buzz_builder, "/api/v1", ["Buzz Builder"]),
    (legal, "/api/v1", ["Legal Assistance"]),
    (exit_strategy_explorer, "/api/v1", ["Exit Strategy Explorer"]),
    (talent_navigator, "/api/v1", ["Talent Navigator"]),
]

for router_module, prefix, tags in routers_config:
    app.include_router(
        router_module.router,
        prefix=prefix,
        tags=tags,
        dependencies=[GLOBAL_DEFAULT_RATE_LIMIT, Depends(get_api_key)]
    )

@app.get("/", summary="Health Check", tags=["System"], dependencies=[GLOBAL_DEFAULT_RATE_LIMIT, Depends(get_api_key)])
async def read_root():
    return {"message": f"Welcome to {settings.APP_NAME} API! Visit /docs for API documentation."}

@app.exception_handler(Exception)
async def catch_all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected server error occurred.", "error_message": str(exc)},
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )