from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = Field("Entrepreneurial Navigator Backend", description="Name of the FastAPI application.")
    REDIS_URL: str = Field("redis://localhost:6379/0", env="REDIS_URL", description="URL for connecting to Redis.")
    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY", description="API Key for Google Gemini.")
    SERPAPI_API_KEY: str = Field(None, env="SERPAPI_API_KEY", description="API Key for SerpAPI (Optional).")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()