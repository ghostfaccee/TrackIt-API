from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import HabitNotFoundError
from app.repositories.log_repository import LogRepository
from app.repositories.habit_repository import HabitRepository
from datetime import datetime, timedelta

class StatsService:
    def __init__(self, db: AsyncSession):
        self.log_repo = LogRepository(db)
        self.habit_repo = HabitRepository(db)
    
    async def _calculate_streak(self, logs: list):
        if not logs: 
            return 0

        sorted_logs = sorted(logs, key = lambda x: x.date, reverse = True)
        streak = 0
        current_date = datetime.now().date()

        for l in sorted_logs:
            if l.date.date() == current_date:
                streak += 1
                current_date -= timedelta(days = 1)
            else: 
                break
        
        return streak

    async def get_stats(self, habit_id: int) -> dict:
        habit = await self.habit_repo.get_by_id(habit_id)
        if not habit:
            raise HabitNotFoundError(habit_id)
        logs = await self.log_repo.get_all_by_habit_id(habit_id)
        total_days = len({log.date.date() for log in logs})
        streak = await self._calculate_streak(logs)
        last_logged = logs[0].date if logs else None
        
        return {
            'total_days' : total_days,
            'streak' : streak,
            'last_logged' : last_logged,
        }
