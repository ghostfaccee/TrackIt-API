from app.core.exceptions import InvalidCredentialsError, UsernameExistsError, EmailExistsError
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import UserRegister, UserLogin
from app.models.users import User
from app.schemas.auth import TokenResponse

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
    
    async def register(self, data: UserRegister) -> User:
        existing = await self.repo.get_by_username(data.username)
        if existing:
            raise UsernameExistsError(data.username)

        if data.email:
            existing = await self.repo.get_by_email(data.email)
            if existing:
                raise EmailExistsError(data.email)
        
        hashed_pwd = hash_password(data.password)
        user = User(
            username = data.username,
            email = data.email,
            hashed_pass = hashed_pwd
        )
        return await self.repo.create(user)
    
    async def login(self, data: UserLogin) -> TokenResponse:
        user = await self.repo.get_by_username(data.username)
        if not user:
            raise InvalidCredentialsError()
        
        if not verify_password(data.password, user.hashed_pass):
            raise InvalidCredentialsError()
        
        token = create_access_token({'sub': str(user.id)})
        return TokenResponse(access_token = token)