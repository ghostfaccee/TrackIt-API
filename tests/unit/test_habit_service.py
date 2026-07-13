import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.habit_service import HabitService
from app.models.users import User
from app.schemas.habit import HabitCreate
from app.core.exceptions import HabitNotFoundError, HabitNameEmptyError

@pytest.mark.asyncio
async def test_create_habit(db_session: AsyncSession, test_user: User):
    habit_service = HabitService(db_session)
    habit_data = HabitCreate(name = 'Test Habit', description = 'Description')
    habit = await habit_service.create(test_user.id, habit_data)
    assert habit.id is not None
    assert habit.user_id is not None
    assert habit.name == 'Test Habit' 
    assert habit.description == 'Description'

@pytest.mark.asyncio
async def test_create_habit_empty_name(db_session: AsyncSession, test_user: User):
    service = HabitService(db_session)
    data = HabitCreate(name = '         ', description = '')
    with pytest.raises(HabitNameEmptyError):
        await service.create(test_user.id, data)

@pytest.mark.asyncio
async def test_get_habit_not_found(db_session: AsyncSession, test_user: User):
    service = HabitService(db_session)
    with pytest.raises(HabitNotFoundError):
        await service.get_by_id(test_user.id, 999)

@pytest.mark.asyncio
async def test_update_habit(db_session: AsyncSession, test_user: User):
    service = HabitService(db_session)
    habit = await service.create(test_user.id, HabitCreate(name = 'Old name', description = 'Old description'))
    updated = await service.update(test_user.id, habit.id, HabitCreate(name = 'New name', description = 'New description'))
    assert updated.name == 'New name' 
    assert updated.description == 'New description'

@pytest.mark.asyncio
async def test_delete_habit(db_session: AsyncSession, test_user: User):
    service = HabitService(db_session)
    habit = await service.create(test_user.id, HabitCreate(name = 'Habit name', description = 'Habit description'))
    await service.delete(test_user.id, habit.id)
    with pytest.raises(HabitNotFoundError):
        await service.get_by_id(test_user.id, habit.id)