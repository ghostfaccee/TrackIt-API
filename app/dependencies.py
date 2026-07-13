from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.exceptions import CouldNotValidateCredentialsError
from app.core.security import decode_token
from app.services.habit_service import HabitService
from app.services.log_service import LogService
from app.services.stats_service import StatsService
from app.services.auth_service import AuthService
from app.services.users_service import UserService
from app.models.users import User

async def get_habit_service(db: AsyncSession = Depends(get_db)) -> HabitService:
    return HabitService(db)

async def get_log_service(db: AsyncSession = Depends(get_db)) -> LogService:
    return LogService(db)

async def get_stats_service(db: AsyncSession = Depends(get_db)) -> StatsService:
    return StatsService(db)

async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/v1/auth/login')
async def get_current_user(token: str = Depends(oauth2_scheme), service: UserService = Depends(get_user_service)) -> User:
    payload = decode_token(token)
    if not payload:
        raise CouldNotValidateCredentialsError()
    user_id = payload.get('sub')
    if not user_id:
        raise CouldNotValidateCredentialsError()
    return await service.get_by_id(int(user_id))
