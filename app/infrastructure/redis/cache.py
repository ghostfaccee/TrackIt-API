from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from app.core.config import settings

class CacheService:
    _enabled = True
    
    @classmethod
    def disable(cls):
        cls._enabled = False
    
    @classmethod
    async def init(cls):
        if not cls._enabled:
            return
        
        redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            max_connections=10
        )
        FastAPICache.init(
            RedisBackend(redis_client),
            prefix="trackit-cache"
        )
    
    @staticmethod
    def cached(expire: int = 60):
        def decorator(func):
            if not CacheService._enabled:
                return func
            
            return cache(expire=expire)(func)
        return decorator
    
    @staticmethod
    async def clear():
        if CacheService._enabled:
            await FastAPICache.clear(namespace="trackit-cache")