# Redis client for caching and storing temporary data. Currently not used in the project and reserved for future innovations.

import redis.asyncio as redis
from app.core.config import settings

class RedisClient:
    _client = None

    @classmethod
    async def get_client(cls) -> redis.Redis:
        if cls._client is None:
            cls._client = redis.from_url(
                settings.REDIS_URL,
                decode_responses = True,
                max_connections = 10
            )
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.aclose()
            cls._client = None

