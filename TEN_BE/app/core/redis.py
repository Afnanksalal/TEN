import redis.asyncio as redis
from redis import exceptions as redis_exceptions
from app.core.config import settings
import asyncio
from typing import Optional

_redis_client: Optional[redis.Redis] = None
_lock = asyncio.Lock()

async def connect_redis():
    """
    Establishes a connection to the Redis server.
    Ensures only one connection attempt at a time.
    """
    global _redis_client
    async with _lock:
        if _redis_client is None:
            try:
                _redis_client = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                )
                await _redis_client.ping()
                print("Successfully connected to Upstash Redis!")
            except redis_exceptions.ConnectionError as e:
                print(f"ERROR: Could not connect to Redis at {settings.REDIS_URL}: {e}. Check URL, credentials, and network.")
                _redis_client = None
            except Exception as e:
                print(f"An unexpected error occurred during Redis connection: {e}")
                _redis_client = None


async def disconnect_redis():
    """
    Closes the connection to the Redis server.
    """
    global _redis_client
    async with _lock:
        if _redis_client:
            print("Disconnecting from Redis...")
            await _redis_client.close()
            _redis_client = None
            print("Redis disconnected.")


async def get_redis_client() -> redis.Redis:
    """
    Returns the global Redis client instance.
    Raises an error if the client has not been initialized.
    """
    if _redis_client is None:
        raise ConnectionError("Redis client is not initialized. Ensure connect_redis() was called successfully.")
    return _redis_client
