import random
import string

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.database import Base, get_db
from app.repositories.user_repository import UserRepository
from app.models.users import User

from app.infrastructure.redis.cache import CacheService
from app.middlewares.rate_limit.limiter import RateLimit

CacheService.disable()
RateLimit.disable_redis()

from app.main import app

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

@pytest.fixture
async def auth(client: AsyncClient):
    rand_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 6))

    username = f'testuser_{rand_suffix}'
    email = f'{username}@test.com'
    password = 'testpass123'

    register_response = await client.post('/v1/auth/register', json = {
        'username' : username,
        'email' : email,
        'password' : password
    })
    assert register_response.status_code == 201, 'Failed to register testuser'

    login_response = await client.post('/v1/auth/login', json = {
        'username' : username,
        'password' : password
    })
    assert login_response.status_code == 200, 'Failed to login testuser'

    token_data = login_response.json()
    assert 'access_token' in token_data, 'No access_token in login_response'

    return token_data['access_token']

@pytest.fixture
async def test_user(db_session: AsyncSession):
    repo = UserRepository(db_session)
    user = User(
        username = 'testuser',
        email = 'email@test.com',
        hashed_pass = 'hashed_test_pass'
    )
    created_user = await repo.create(user)
    return created_user