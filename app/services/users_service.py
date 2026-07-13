from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.models.users import User
from app.core.exceptions import UserNotFoundError
from typing import Optional

class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user
    