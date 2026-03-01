import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.dependencies import get_db
from app.core.config import settings

# Test Database URL (using a separate test database or postgres in docker)
TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    settings.POSTGRES_DB, f"{settings.POSTGRES_DB}_test"
)

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture(autouse=True)
async def setup_db():
    # In a real scenario, we'd run migrations here or create all tables
    # For now, we assume the test runner handles DB creation/migrations
    yield
