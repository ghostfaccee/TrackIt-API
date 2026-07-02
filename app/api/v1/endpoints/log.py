from fastapi import APIRouter, Depends, status
from app.dependencies import get_log_service
from app.services.log_service import LogService
from app.schemas.log import LogCreate
from app.schemas.log import LogResponse

router = APIRouter()

@router.post('/log/{habit_id}', response_model = LogResponse, status_code = status.HTTP_201_CREATED)
async def create(habit_id: int, data: LogCreate, service: LogService = Depends(get_log_service)):
    return await service.create(habit_id, data)

@router.delete('/log/{log_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete(log_id: int, service: LogService = Depends(get_log_service)):
    await service.delete(log_id)
    return None
