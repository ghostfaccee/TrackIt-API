import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.habit_service import HabitService
from app.services.stats_service import StatsService
from app.services.log_service import LogService
from app.schemas.habit import HabitCreate
from app.schemas.log import LogCreate
from app.core.exceptions import HabitNotFoundError

@pytest.mark.asyncio
async def test_stats_unique_days(db_session: AsyncSession):
    habit_service = HabitService(db_session)
    stats_service = StatsService(db_session)
    log_service = LogService(db_session)

    habit = await habit_service.create(HabitCreate(name = 'Habit'))
    for _ in range(3):
        await log_service.create(habit.id, LogCreate(completed = True))
    
    stats = await stats_service.get_stats(habit.id)

    assert stats['total_days'] == 1 
    assert stats['streak'] == 1

@pytest.mark.asyncio
async def test_stats_no_logs(db_session: AsyncSession):
    habit_service = HabitService(db_session)
    stats_service = StatsService(db_session)

    habit = await habit_service.create(HabitCreate(name = 'Habit'))
    stats = await stats_service.get_stats(habit.id)

    assert stats['total_days'] == 0 
    assert stats['streak'] == 0

@pytest.mark.asyncio
async def test_stats_habit_not_found(db_session: AsyncSession):
    stats_service = StatsService(db_session)
    with pytest.raises(HabitNotFoundError):
        await stats_service.get_stats(999)
