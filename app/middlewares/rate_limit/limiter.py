from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, status
from app.core.config import settings
from fastapi.responses import JSONResponse

class RateLimit:
    _enabled_redis = True

    @classmethod
    def disable_redis(cls):
        cls._enabled_redis = False

    @classmethod
    def get_limiter(cls):
        if not cls._enabled_redis:
            return Limiter(
                key_func = get_remote_address,
                default_limits = ['20/minute'],
                enabled = False # Disabling limits for tests
            )
        return Limiter(
            key_func = get_remote_address,
            storage_uri = settings.REDIS_URL,
            default_limits = ['20/minute']
        )

    @staticmethod
    def rate_limit_exceed_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code = status.HTTP_429_TOO_MANY_REQUESTS,
            content = {'detail' : 'Too many requests.'}
        )

