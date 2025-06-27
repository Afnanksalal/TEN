from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.v1.routers import risk, reputation, matching, competitor_radar, traction_estimator, buzz_builder, legal
from app.core.config import settings
from app.core.redis import connect_redis, disconnect_redis
from app.core.gemini_client import init_gemini_model
import uvicorn

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="An AI-powered platform to assist first-time entrepreneurs with risk assessment, reputation analysis, and investor matching.",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    print("Application startup event: Connecting to Redis...")
    await connect_redis()
    print("Application startup event: Initializing Gemini model...")
    init_gemini_model()
    print("Startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    print("Application shutdown event: Disconnecting from Redis...")
    await disconnect_redis()
    print("Shutdown complete.")

app.include_router(risk.router, prefix="/api/v1", tags=["Risk Assessment"])
app.include_router(reputation.router, prefix="/api/v1", tags=["Reputation Analysis"])
app.include_router(matching.router, prefix="/api/v1", tags=["Investor Matching & Pitch Feedback"])
app.include_router(competitor_radar.router, prefix="/api/v1", tags=["Competitor Radar"])
app.include_router(traction_estimator.router, prefix="/api/v1", tags=["Traction Estimator"])
app.include_router(buzz_builder.router, prefix="/api/v1", tags=["Buzz Builder"])
app.include_router(legal.router, prefix="/api/v1", tags=["Legal Assistance"])

@app.get("/", summary="Health Check", tags=["System"])
async def read_root():
    return {"message": f"Welcome to {settings.APP_NAME} API! Visit /docs for API documentation."}

@app.exception_handler(Exception)
async def catch_all_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception caught: {exc}")
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