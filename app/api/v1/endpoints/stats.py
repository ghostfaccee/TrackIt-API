from fastapi import APIRouter, Depends, Request
from app.dependencies import get_stats_service
from app.services.stats_service import StatsService
from app.schemas.stats import StatsResponse
from app.middlewares.rate_limit.limiter import RateLimit
from app.infrastructure.redis.cache import CacheService
from app.dependencies import get_current_user
from app.models.users import User

router = APIRouter()
limiter = RateLimit.get_limiter()

@router.get('/stats/{habit_id}', response_model = StatsResponse)
@CacheService.cached(expire = 50)
@limiter.limit('15/minute')
async def get(request: Request, habit_id: int, user: User = Depends(get_current_user), service: StatsService = Depends(get_stats_service)):
    return await service.get_stats(user.id, habit_id)