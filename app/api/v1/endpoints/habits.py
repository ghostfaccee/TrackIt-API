from typing import List
from fastapi import APIRouter, Depends, status, Request
from app.dependencies import get_habit_service, get_current_user
from app.services.habit_service import HabitService
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse
from app.middlewares.rate_limit.limiter import RateLimit
from app.infrastructure.redis.cache import CacheService
from app.models.users import User

router = APIRouter()
limiter = RateLimit.get_limiter()

@router.get('/habits', response_model = List[HabitResponse], summary = 'Habits', description = 'Returns a list of all the user\'s habits. Requires a jwt token.')
@CacheService.cached(expire = 50)
@limiter.limit('15/minute')
async def get_all(request: Request, user: User = Depends(get_current_user), service: HabitService = Depends(get_habit_service)):
    return await service.get_all(user.id)

@router.post('/habit/create', response_model = HabitResponse, status_code = status.HTTP_201_CREATED, summary = 'Create a habit', description = 'Creates a habit for the user. Requires a jwt token.')
@limiter.limit('15/minute')
async def create(request: Request, data: HabitCreate, user: User = Depends(get_current_user), service: HabitService = Depends(get_habit_service)):
    await CacheService.clear()
    return await service.create(user.id, data)

@router.get('/habit/{habit_id}', response_model = HabitResponse, summary = 'Get a habit by id', description = 'Allows you to get a habit by id. Requires a jwt token.')
@CacheService.cached(expire = 50)
@limiter.limit('15/minute')
async def get_by_id(request: Request, habit_id: int, user: User = Depends(get_current_user), service: HabitService = Depends(get_habit_service)):
    return await service.get_by_id(user.id, habit_id)

@router.delete('/habit/{habit_id}', status_code = status.HTTP_204_NO_CONTENT, summary = 'Delete a habit by id', description = 'Removes a habit by id. Requires a jwt token.')
@limiter.limit('15/minute')
async def delete_by_id(request: Request, habit_id: int, user: User = Depends(get_current_user), service: HabitService = Depends(get_habit_service)):
    await service.delete(user.id, habit_id)
    await CacheService.clear()
    return None

@router.put('/habit/{habit_id}', response_model = HabitResponse, summary = 'Update habit by id', description = 'Updates the habit by id. Requires a jwt token.')
@limiter.limit('15/minute')
async def update(request: Request, habit_id: int, data: HabitUpdate, user: User = Depends(get_current_user), service: HabitService = Depends(get_habit_service)):
    await CacheService.clear()
    return await service.update(user.id, habit_id, data)

