from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    SLOW_REQUEST_THRESHOLD: float
    DEBUG: bool = True

    model_config = ConfigDict(env_file = '.env', case_sensitive = True)

settings = Settings()
