from fastapi import status
from fastapi import APIRouter, Depends, Request
from app.dependencies import get_auth_service
from app.middlewares.rate_limit.limiter import RateLimit
from app.schemas.auth import UserRegister, UserLogin
from app.schemas.auth import TokenResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()
limiter = RateLimit.get_limiter()

@router.post('/auth/register', response_model = UserResponse, status_code = status.HTTP_201_CREATED, summary = 'Registration', description = 'Creates a new user. Returns the user\'s username and email.')
@limiter.limit('5/minute')
async def register(request: Request, data: UserRegister, service: AuthService = Depends(get_auth_service)):
    return await service.register(data)

@router.post('/auth/login', response_model = TokenResponse, summary = 'Login', description = 'User login. Returns the jwt token required for other endpoints and its type.')
@limiter.limit('5/minute')
async def login(request: Request, data: UserLogin, service: AuthService = Depends(get_auth_service)):
    return await service.login(data)

