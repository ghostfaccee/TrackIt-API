from fastapi import APIRouter, Depends, status, Request
from typing import List
from app.dependencies import get_habit_service
from app.services.habit_service import HabitService
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse
from app.middlewares.rate_limit.limiter import RateLimit
from app.infrastructure.redis.cache import CacheService

router = APIRouter()
limiter = RateLimit.get_limiter()

@router.get('/habits', response_model = List[HabitResponse])
@CacheService.cached(expire = 50)
@limiter.limit('15/minute')
async def get_all(request: Request, service: HabitService = Depends(get_habit_service)):
    return await service.get_all()

@router.post('/habit/create', response_model = HabitResponse, status_code = status.HTTP_201_CREATED)
@limiter.limit('15/minute')
async def create(request: Request, data: HabitCreate, service: HabitService = Depends(get_habit_service)):
    await CacheService.clear()
    return await service.create(data)

@router.get('/habit/{habit_id}', response_model = HabitResponse)
@CacheService.cached(expire = 50)
@limiter.limit('15/minute')
async def get_by_id(request: Request, habit_id: int, service: HabitService = Depends(get_habit_service)):
    return await service.get_by_id(habit_id)

@router.delete('/habit/{habit_id}', status_code = status.HTTP_204_NO_CONTENT)
@limiter.limit('15/minute')
async def delete_by_id(request: Request, habit_id: int, service: HabitService = Depends(get_habit_service)):
    await service.delete(habit_id)
    await CacheService.clear()
    return None

@router.put('/habit/{habit_id}', response_model = HabitResponse)
@limiter.limit('15/minute')
async def update(request: Request, habit_id: int, data: HabitUpdate, service: HabitService = Depends(get_habit_service)):
    await CacheService.clear()
    return await service.update(habit_id, data)

