import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Base
from src.database.session import Connector
from src.configuration.config import settings

test_db_connector = Connector(
    url=str(settings.db.test_db_url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with test_db_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_db_connector.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
async def session() -> AsyncSession:
    async with test_db_connector.session_factory() as session:
        yield session
