from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import List

from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    configured_valid_keys: List[str] = []

    if settings.API_KEY:
        configured_valid_keys.append(settings.API_KEY)
    elif settings.VALID_API_KEYS:
        configured_valid_keys.extend(settings.VALID_API_KEYS)

    if not configured_valid_keys:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: No API keys defined."
        )

    if api_key not in configured_valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key