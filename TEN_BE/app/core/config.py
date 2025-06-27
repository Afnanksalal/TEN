from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = Field("The Entrepreneurial Navigator", description="Name of the FastAPI application.")
    REDIS_URL: str = Field("redis://localhost:6379/0", env="REDIS_URL", description="URL for connecting to Redis.")
    GOOGLE_API_KEY: str = Field(..., env="GOOGLE_API_KEY", description="API Key for Google Gemini.")
    SERPAPI_API_KEY: str = Field(None, env="SERPAPI_API_KEY", description="API Key for SerpAPI (Optional).")

    API_KEY: Optional[str] = Field(None, env="API_KEY")
    VALID_API_KEYS: List[str] = Field(default_factory=list, env="VALID_API_KEYS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()