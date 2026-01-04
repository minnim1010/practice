import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database import Base
from app.team.service import (
    add_team,
    get_teams,
    get_team,
    update_team,
    delete_team,
)
from app.team.dto import TeamCreate, TeamUpdate

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def test_db_session():
    """
    Fixture to set up an in-memory database for each test function.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    TestAsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(autouse=True)
def override_db_session(monkeypatch, test_db_session):
    """
    Fixture to automatically replace AsyncSessionLocal with the test database session.
    """
    monkeypatch.setattr(
        "app.team.service.AsyncSessionLocal",
        lambda: test_db_session,
    )


async def test_add_team():
    team_create_data = TeamCreate(
        squad_name="Test Squad",
        squad_lead="Test Lead",
        tribe="Test Tribe",
        tribe_lead="Test Tribe Lead",
        product_line="Test Product",
        dh_slack_group="test-slack",
    )

    created_team = await add_team(team_create_data)

    assert created_team.id is not None
    assert created_team.squad_name == "Test Squad"

    retrieved_team = await get_team(created_team.id)
    assert retrieved_team.squad_name == "Test Squad"


async def test_get_teams():
    team1_data = TeamCreate(
        squad_name="Squad 1",
        squad_lead="Lead 1",
        tribe="Tribe 1",
        tribe_lead="TLead 1",
        product_line="PL 1",
        dh_slack_group="slack1",
    )
    team2_data = TeamCreate(
        squad_name="Squad 2",
        squad_lead="Lead 2",
        tribe="Tribe 2",
        tribe_lead="TLead 2",
        product_line="PL 2",
        dh_slack_group="slack2",
    )
    await add_team(team1_data)
    await add_team(team2_data)

    teams = await get_teams()

    assert len(teams) == 2
    assert teams[0].squad_name == "Squad 1"
    assert teams[1].squad_name == "Squad 2"


async def test_get_team():
    team_data = TeamCreate(
        squad_name="Test Squad",
        squad_lead="Lead",
        tribe="Tribe",
        tribe_lead="TLead",
        product_line="PL",
        dh_slack_group="slack",
    )
    created_team = await add_team(team_data)

    retrieved_team = await get_team(created_team.id)

    assert retrieved_team is not None
    assert retrieved_team.id == created_team.id
    assert retrieved_team.squad_name == "Test Squad"


async def test_get_team_not_found():
    with pytest.raises(ValueError, match="Team with id 999 not found."):
        await get_team(999)


async def test_update_team():
    team_data = TeamCreate(
        squad_name="Old Squad Name",
        squad_lead="Old Lead",
        tribe="Old Tribe",
        tribe_lead="Old TLead",
        product_line="Old PL",
        dh_slack_group="old-slack",
    )
    created_team = await add_team(team_data)
    update_data = TeamUpdate(squad_name="New Squad Name")

    await update_team(team_id=created_team.id, team_values=update_data)

    updated_team = await get_team(created_team.id)
    assert updated_team.squad_name == "New Squad Name"


async def test_delete_team():
    team_data = TeamCreate(
        squad_name="Squad to Delete",
        squad_lead="Lead",
        tribe="Tribe",
        tribe_lead="TLead",
        product_line="PL",
        dh_slack_group="slack",
    )
    created_team = await add_team(team_data)

    await delete_team(created_team.id)

    with pytest.raises(ValueError):
        await get_team(created_team.id)
