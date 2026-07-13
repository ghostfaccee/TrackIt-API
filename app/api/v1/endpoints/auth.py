from fastapi import APIRouter, Depends, Request
from app.dependencies import get_auth_service
from fastapi import status
from app.middlewares.rate_limit.limiter import RateLimit
from app.schemas.auth import UserRegister, UserLogin
from app.services.auth_service import AuthService
from app.schemas.auth import TokenResponse, UserResponse

router = APIRouter()
limiter = RateLimit.get_limiter()

@router.post('/auth/register', response_model = UserResponse, status_code = status.HTTP_201_CREATED)
@limiter.limit('5/minute')
async def register(request: Request, data: UserRegister, service: AuthService = Depends(get_auth_service)):
    return await service.register(data)

@router.post('/auth/login', response_model = TokenResponse)
@limiter.limit('5/minute')
async def login(request: Request, data: UserLogin, service: AuthService = Depends(get_auth_service)):
    return await service.login(data)