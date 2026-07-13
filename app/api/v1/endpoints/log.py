from fastapi import APIRouter, Depends, status, Request
from app.dependencies import get_log_service
from app.services.log_service import LogService
from app.schemas.log import LogCreate
from app.schemas.log import LogResponse
from app.middlewares.rate_limit.limiter import RateLimit
from app.dependencies import get_current_user
from app.models.users import User

router = APIRouter()
limiter = RateLimit.get_limiter()

@router.post('/log/{habit_id}', response_model = LogResponse, status_code = status.HTTP_201_CREATED)
@limiter.limit('1/day')
async def create(request: Request, habit_id: int, data: LogCreate, user: User = Depends(get_current_user), service: LogService = Depends(get_log_service)):
    return await service.create(user.id, habit_id, data)

@router.delete('/log/{log_id}', status_code = status.HTTP_204_NO_CONTENT)
@limiter.limit('15/minute')
async def delete(request: Request, log_id: int, user: User = Depends(get_current_user), service: LogService = Depends(get_log_service)):
    await service.delete(user.id, log_id)
    return None
