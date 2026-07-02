import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.habit_service import HabitService
from app.schemas.habit import HabitCreate
from app.core.exceptions import HabitNotFoundError, HabitNameEmptyError

@pytest.mark.asyncio
async def test_create_habit(db_session: AsyncSession):
    service = HabitService(db_session)
    data = HabitCreate(name = 'Test Habit', description = 'Description')
    habit = await service.create(data)
    assert habit.id is not None
    assert habit.name == 'Test Habit' 
    assert habit.description == 'Description'

@pytest.mark.asyncio
async def test_create_habit_empty_name(db_session: AsyncSession):
    service = HabitService(db_session)
    data = HabitCreate(name = '         ', description = '')
    with pytest.raises(HabitNameEmptyError):
        await service.create(data)

@pytest.mark.asyncio
async def test_get_habit_not_found(db_session: AsyncSession):
    service = HabitService(db_session)
    with pytest.raises(HabitNotFoundError):
        await service.get_by_id(999)

@pytest.mark.asyncio
async def test_update_habit(db_session: AsyncSession):
    service = HabitService(db_session)
    habit = await service.create(HabitCreate(name = 'Old name', description = 'Old description'))
    updated = await service.update(habit.id, HabitCreate(name = 'New name', description = 'New description'))
    assert updated.name == 'New name' 
    assert updated.description == 'New description'

@pytest.mark.asyncio
async def test_delete_habit(db_session: AsyncSession):
    service = HabitService(db_session)
    habit = await service.create(HabitCreate(name = 'Habit name', description = 'Habit description'))
    await service.delete(habit.id)
    with pytest.raises(HabitNotFoundError):
        await service.get_by_id(habit.id)