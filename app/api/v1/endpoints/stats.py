from fastapi import APIRouter, Depends
from app.dependencies import get_stats_service
from app.services.stats_service import StatsService
from app.schemas.stats import StatsResponse

router = APIRouter()

@router.get('/stats/{habit_id}', response_model = StatsResponse)
async def get(habit_id: int, service: StatsService = Depends(get_stats_service)):
    return await service.get_stats(habit_id)