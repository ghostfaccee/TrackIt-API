from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.habit_repository import HabitRepository
from app.repositories.log_repository import LogRepository
from app.schemas.log import LogCreate
from app.core.exceptions import LogNotFoundError, HabitNotFoundError, PermissionDeniedError
from app.models.log import Log

class LogService:
    def __init__(self, db: AsyncSession):
        self.log_repo = LogRepository(db)
        self.habit_repo = HabitRepository(db)
    
    async def create(self, user_id: int, habit_id: int, data: LogCreate) -> Log:
        habit = await self.habit_repo.get_by_id(user_id, habit_id)
        if not habit:
            raise HabitNotFoundError(habit_id)
        return await self.log_repo.create(habit_id, data)
    
    async def delete(self, user_id: int, log_id: int) -> None:
        log = await self.log_repo.get_by_id(log_id)
        if not log:
            raise LogNotFoundError(log_id)
        if not await self.habit_repo.get_by_id(user_id, log.habit_id):
            raise PermissionDeniedError
        await self.log_repo.delete(log_id)
        return None
    
