from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.users import User
from typing import Optional

class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_username(self, username: str) -> Optional[User]:
        user = await self.db.execute(select(User).where(User.username == username))
        return user.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        user = await self.db.execute(select(User).where(User.email == email))
        return user.scalar_one_or_none()
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        user = await self.db.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()
