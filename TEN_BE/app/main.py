from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api.v1.routers import risk, reputation, matching # Import all your API routers
from app.core.config import settings
from app.core.redis import connect_redis, disconnect_redis # Import Redis connection functions
import uvicorn # Used to run the app programmatically (optional, but good for testing)

# Initialize the FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="An AI-powered platform to assist first-time entrepreneurs with risk assessment, reputation analysis, and investor matching.",
    docs_url="/docs",       # Swagger UI documentation
    redoc_url="/redoc"      # ReDoc documentation
)

# --- Application Lifecycle Events ---

@app.on_event("startup")
async def startup_event():
    """
    Connect to Redis when the application starts up.
    """
    print("Application startup event: Connecting to Redis...")
    await connect_redis()
    print("Startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Disconnect from Redis when the application shuts down.
    """
    print("Application shutdown event: Disconnecting from Redis...")
    await disconnect_redis()
    print("Shutdown complete.")

# --- Include API Routers ---
# These lines attach the defined endpoints from your router files to the main FastAPI app.
app.include_router(risk.router, prefix="/api/v1", tags=["Risk Assessment"])
app.include_router(reputation.router, prefix="/api/v1", tags=["Reputation Analysis"])
app.include_router(matching.router, prefix="/api/v1", tags=["Investor Matching & Pitch Feedback"])

# --- Root Endpoint (Optional, for simple health check) ---
@app.get("/", summary="Health Check", tags=["System"])
async def read_root():
    """
    A simple endpoint to check if the API is running.
    """
    return {"message": f"Welcome to {settings.APP_NAME} API! Visit /docs for API documentation."}

# --- Optional: Custom Exception Handler ---
# This is a good practice for hackathons to catch unexpected errors and return a clean JSON.
@app.exception_handler(Exception)
async def catch_all_exception_handler(request: Request, exc: Exception):
    """
    Generic exception handler to catch any unhandled exceptions.
    """
    print(f"Unhandled exception caught: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected server error occurred.", "error_message": str(exc)},
    )

# --- How to run the application directly (for local development/testing) ---
# This block is typically used when you run the script directly: `python app/main.py`
# In production or with Docker, you'd use `uvicorn app.main:app --host 0.0.0.0 --port 8000`
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )