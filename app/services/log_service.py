from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.habit_repository import HabitRepository
from app.repositories.log_repository import LogRepository
from app.schemas.log import LogCreate
from app.core.exceptions import LogNotFoundError, HabitNotFoundError
from app.models.log import Log

class LogService:
    def __init__(self, db: AsyncSession):
        self.log_repo = LogRepository(db)
        self.habit_repo = HabitRepository(db)
    
    async def create(self, habit_id: int, data: LogCreate) -> Log:
        habit = await self.habit_repo.get_by_id(habit_id)
        if not habit:
            raise HabitNotFoundError(habit_id)
        return await self.log_repo.create(habit_id, data)
    
    async def delete(self, log_id: int) -> None:
        if not await self.log_repo.delete(log_id):
            raise LogNotFoundError(log_id)
        return None
    
