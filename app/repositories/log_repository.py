from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.log import Log
from app.schemas.log import LogCreate

class LogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, habit_id: int, data: LogCreate) -> Log:
        log = Log(habit_id = habit_id, **data.model_dump())
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log
    
    async def get_all_by_habit_id(self, habit_id: int) -> Optional[Log]:
        result = await self.db.execute(select(Log).where(Log.habit_id == habit_id).order_by(Log.date.desc()))
        return result.scalars().all()
    
    async def get_by_id(self, log_id: int) -> Optional[Log]:
        result = await self.db.execute(select(Log).where(Log.id == log_id))
        return result.scalar_one_or_none()

    async def delete(self, log_id: int) -> bool:
        log = await self.db.get(Log, log_id)
        if log:
            await self.db.delete(log)
            await self.db.commit()
            return True
        return False