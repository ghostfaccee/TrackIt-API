from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite+aiosqlite:///./trackit.db'
    DEBUG: bool = True

    model_config = ConfigDict(env_file = '.env', case_sensetive = True)

settings = Settings()
