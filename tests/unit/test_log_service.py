import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.log_service import LogService
from app.services.habit_service import HabitService
from app.schemas.log import LogCreate
from app.schemas.habit import HabitCreate
from app.core.exceptions import LogNotFoundError

@pytest.mark.asyncio
async def test_log_create(db_session: AsyncSession):
    habit_service = HabitService(db_session)
    log_service = LogService(db_session)
    habit = await habit_service.create(HabitCreate(name = 'Habit'))
    log = await log_service.create(habit.id, LogCreate(completed = False))
    assert log.id is not None
    assert log.completed == False

@pytest.mark.asyncio
async def test_log_delete(db_session: AsyncSession):
    habit_service = HabitService(db_session)
    log_service = LogService(db_session)
    habit = await habit_service.create(HabitCreate(name = 'Habit'))
    log = await log_service.create(habit.id, LogCreate())
    await log_service.delete(log.id)
    with pytest.raises(LogNotFoundError):
        await log_service.delete(log.id)