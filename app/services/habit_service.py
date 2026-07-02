from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.repositories.habit_repository import HabitRepository
from app.schemas.habit import HabitCreate, HabitUpdate
from app.core.exceptions import HabitNotFoundError, HabitNameEmptyError
from app.models.habit import Habit

class HabitService:
    def __init__(self, db: AsyncSession):
        self.repo = HabitRepository(db)
    
    async def get_all(self) -> List[Habit]:
        return await self.repo.get_all()
    
    async def get_by_id(self, habit_id: int) -> Habit:
        habit = await self.repo.get_by_id(habit_id)
        if not habit:
            raise HabitNotFoundError(habit_id)
        return habit
    
    async def create(self, data: HabitCreate) -> Habit:
        if not data.name or not data.name.strip():
            raise HabitNameEmptyError()
        return await self.repo.create(data)

    async def update(self, habit_id: int, data: HabitUpdate) -> Habit:
        await self.get_by_id(habit_id)
        updated = await self.repo.update(habit_id, data)
        if not updated:
            raise HabitNotFoundError(habit_id)
        return updated
        
    async def delete(self, habit_id: int) -> None:
        if not await self.repo.delete(habit_id):
            raise HabitNotFoundError(habit_id)
        return None
