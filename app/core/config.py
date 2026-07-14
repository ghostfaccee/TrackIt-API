from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    REDIS_URL: str

    SLOW_REQUEST_THRESHOLD: float

    DEBUG: bool = True

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = ConfigDict(env_file = '.env', case_sensitive = True)

settings = Settings()
