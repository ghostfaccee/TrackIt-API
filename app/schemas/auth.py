from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    username: str = Field(..., min_length = 3, max_length = 30)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length = 6)

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class UserResponse(BaseModel):
    username: str
    email: Optional[str]