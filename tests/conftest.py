import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.database import Base, get_db

from app.infrastructure.redis.cache import CacheService
CacheService.disable()

import app.middlewares.rate_limit.limiter as rate_limit_module
from slowapi import Limiter
from slowapi.util import get_remote_address

def mock_limit(self, limit_str: str):
    def decorator(func):
        return func
    return decorator

rate_limit_module.limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"]
)
rate_limit_module.limiter.limit = mock_limit.__get__(rate_limit_module.limiter, Limiter)

from app.main import app

app.state.limiter = rate_limit_module.limiter

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client