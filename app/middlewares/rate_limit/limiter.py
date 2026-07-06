from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, status
import redis.asyncio as redis
from app.core.config import settings
from fastapi.responses import JSONResponse

limiter = Limiter(
    key_func = get_remote_address,
    storage_uri = settings.REDIS_URL,
    default_limits = ['20/minute']
)

def rate_limit_exceed_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code = status.HTTP_429_TOO_MANY_REQUESTS,
        content = {'detail' : 'Too many requests.'}
    )

