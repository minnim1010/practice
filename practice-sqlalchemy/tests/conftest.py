import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database import Base
import app.models

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def test_db_session():
    """
    Fixture to set up an in-memory database for each test function.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    TestAsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def seed_teams(test_db_session):
    team1 = app.models.Team(
        id=1,
        squad_name="Team 1",
        squad_lead="Lead 1",
        tribe="Tribe 1",
        tribe_lead="Tribe Lead 1",
        product_line="Product 1",
        dh_slack_group="team-1",
    )
    team2 = app.models.Team(
        id=2,
        squad_name="Team 2",
        squad_lead="Lead 2",
        tribe="Tribe 2",
        tribe_lead="Tribe Lead 2",
        product_line="Product 2",
        dh_slack_group="team-2",
    )

    test_db_session.add_all([team1, team2])
    await test_db_session.commit()
