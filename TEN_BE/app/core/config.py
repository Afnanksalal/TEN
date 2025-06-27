from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = Field("Entrepreneurial Navigator Backend", description="Name of the FastAPI application.")
    REDIS_URL: str = Field("redis://localhost:6379/0", env="REDIS_URL", description="URL for connecting to Redis.")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()