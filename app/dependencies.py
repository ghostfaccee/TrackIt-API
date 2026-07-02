from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.habit_service import HabitService
from app.services.log_service import LogService
from app.services.stats_service import StatsService

async def get_habit_service(db: AsyncSession = Depends(get_db)) -> HabitService:
    return HabitService(db)

async def get_log_service(db: AsyncSession = Depends(get_db)) -> LogService:
    return LogService(db)

async def get_stats_service(db: AsyncSession = Depends(get_db)) -> StatsService:
    return StatsService(db)

