from fastapi import APIRouter, Depends, status
from typing import List
from app.dependencies import get_habit_service
from app.services.habit_service import HabitService
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse

router = APIRouter()

@router.get('/habits', response_model = List[HabitResponse])
async def get_all(service: HabitService = Depends(get_habit_service)):
    return await service.get_all()

@router.post('/habit/create', response_model = HabitResponse, status_code = status.HTTP_201_CREATED)
async def create(data: HabitCreate, service: HabitService = Depends(get_habit_service)):
    return await service.create(data)

@router.get('/habit/{habit_id}', response_model = HabitResponse)
async def get_by_id(habit_id: int, service: HabitService = Depends(get_habit_service)):
    return await service.get_by_id(habit_id)

@router.delete('/habit/{habit_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_by_id(habit_id: int, service: HabitService = Depends(get_habit_service)):
    await service.delete(habit_id)
    return None

@router.put('/habit/{habit_id}', response_model = HabitResponse)
async def update(habit_id: int, data: HabitUpdate, service: HabitService = Depends(get_habit_service)):
    return await service.update(habit_id, data)

