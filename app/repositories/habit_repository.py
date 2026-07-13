from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate

class HabitRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self, user_id: int) -> List[Habit]:
        result = await self.db.execute(select(Habit).where(Habit.user_id == user_id))
        return result.scalars().all()
    
    async def get_by_id(self, user_id: int, habit_id: int) -> Optional[Habit]:
        result = await self.db.execute(select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id))
        return result.scalar_one_or_none()
    
    async def update(self, user_id: int, habit_id: int, data: HabitUpdate) -> Optional[Habit]:
        habit = await self.get_by_id(user_id, habit_id)
        if not habit: 
            return None
        for key, value in data.model_dump(exclude_unset = True).items():
            setattr(habit, key, value)
        await self.db.commit()
        await self.db.refresh(habit)
        return habit
    
    async def create(self, user_id: int, data: HabitCreate) -> Habit:
        habit = Habit(user_id = user_id, **data.model_dump())
        self.db.add(habit)
        await self.db.commit()
        await self.db.refresh(habit)
        return habit
    
    async def delete(self, user_id: int, habit_id: int) -> bool:
        habit = await self.get_by_id(user_id, habit_id)
        if habit:
            await self.db.delete(habit)
            await self.db.commit()
            return True
        return False

