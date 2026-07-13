from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings
from typing import Optional
import bcrypt

# passwords
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# jwt
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp' : expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
    except JWTError:
        return None
