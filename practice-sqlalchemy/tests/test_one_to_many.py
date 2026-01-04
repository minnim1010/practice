import pytest
import pytest_asyncio
import sqlalchemy.exc
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from app.application.model import Application
from app.application.service import get_applications
from app.team.model import Team


@pytest_asyncio.fixture(autouse=True)
def override_db_session(monkeypatch, test_db_session):
    monkeypatch.setattr(
        "app.team.service.AsyncSessionLocal",
        lambda: test_db_session,
    )
    monkeypatch.setattr(
        "app.application.service.AsyncSessionLocal",
        lambda: test_db_session,
    )


async def test_one_to_many_create(test_db_session):
    async with test_db_session.begin():
        team = Team(
            squad_name="Test Squad",
            squad_lead="Test Lead",
            tribe="Test Tribe",
            tribe_lead="Test Tribe Lead",
            product_line="Test Product",
            dh_slack_group="test-slack",
        )
        team.applications.append(Application(name="application1"))
        team.applications.append(Application(name="application2"))
        test_db_session.add(team)
    await test_db_session.refresh(team)
    assert team.id is not None

    applications = await get_applications()
    assert len(applications) == 2
    assert applications[0].name == "application1"
    assert applications[1].name == "application2"


async def test_one_to_many_lazy_loading_with_raise_on_sql(test_db_session):
    async with test_db_session.begin():
        team = Team(
            squad_name="Test Squad",
            squad_lead="Test Lead",
            tribe="Test Tribe",
            tribe_lead="Test Tribe Lead",
            product_line="Test Product",
            dh_slack_group="test-slack",
        )
        team.applications.append(Application(name="application1"))
        team.applications.append(Application(name="application2"))
        test_db_session.add(team)
    await test_db_session.refresh(team)
    assert team.id is not None

    with pytest.raises(sqlalchemy.exc.InvalidRequestError):  # Due to lazy='raise_on_sql'
        assert team.applications[0].name == "application1"


async def test_one_to_many_eager_loading(test_db_session):
    """
    SELECT teams.id, teams.squad_name, teams.squad_lead, teams.tribe, teams.tribe_lead, teams.product_line, teams.dh_slack_group
    FROM teams
    SELECT applications.team_id AS applications_team_id, applications.id AS applications_id, applications.name AS applications_name, applications.description AS applications_description
    FROM applications
    WHERE applications.team_id IN (?)
    """
    async with test_db_session.begin():
        team = Team(
            squad_name="Test Squad",
            squad_lead="Test Lead",
            tribe="Test Tribe",
            tribe_lead="Test Tribe Lead",
            product_line="Test Product",
            dh_slack_group="test-slack",
        )
        team.applications.append(Application(name="application1"))
        team.applications.append(Application(name="application2"))
        test_db_session.add(team)

    result = await test_db_session.execute(select(Team).options(selectinload(Team.applications)))
    team = result.scalar_one()

    assert team.id is not None
    assert team.applications[0].name == "application1"
    assert team.applications[1].name == "application2"


async def test_one_to_many_joinedload(test_db_session):
    """
    SELECT teams.id, teams.squad_name, teams.squad_lead, teams.tribe, teams.tribe_lead, teams.product_line, teams.dh_slack_group, applications_1.id AS id_1, applications_1.name, applications_1.description, applications_1.team_id
    FROM teams LEFT OUTER JOIN applications AS applications_1 ON teams.id = applications_1.team_id
    """
    async with test_db_session.begin():
        team = Team(
            squad_name="Test Squad",
            squad_lead="Test Lead",
            tribe="Test Tribe",
            tribe_lead="Test Tribe Lead",
            product_line="Test Product",
            dh_slack_group="test-slack",
        )
        team.applications.append(Application(name="application1"))
        team.applications.append(Application(name="application2"))
        test_db_session.add(team)

    result = await test_db_session.execute(select(Team).options(joinedload(Team.applications)))
    team = result.unique().scalar_one()

    assert team.id is not None
    assert team.applications[0].name == "application1"
    assert team.applications[1].name == "application2"


async def test_one_to_many_joinedload_is_bad_with_pagination(test_db_session):
    """
    SELECT anon_1.id, anon_1.squad_name, anon_1.squad_lead, anon_1.tribe, anon_1.tribe_lead, anon_1.product_line, anon_1.dh_slack_group, applications_1.id AS id_1, applications_1.name, applications_1.description, applications_1.team_id
    FROM (SELECT teams.id AS id, teams.squad_name AS squad_name, teams.squad_lead AS squad_lead, teams.tribe AS tribe, teams.tribe_lead AS tribe_lead, teams.product_line AS product_line, teams.dh_slack_group AS dh_slack_group
    FROM teams
    LIMIT ? OFFSET ?) AS anon_1 LEFT OUTER JOIN applications AS applications_1 ON anon_1.id = applications_1.team_id
    """
    async with test_db_session.begin():
        teams = []
        for i in range(1, 10):
            team = Team(
                squad_name=f"Test Squad_{i}",
                squad_lead="Test Lead",
                tribe="Test Tribe",
                tribe_lead="Test Tribe Lead",
                product_line="Test Product",
                dh_slack_group="test-slack",
            )
            team.applications.append(Application(name=f"application_{i}_1"))
            team.applications.append(Application(name=f"application_{i}_2"))
            teams.append(team)
        test_db_session.add_all(teams)

    result = await test_db_session.execute(select(Team).options(joinedload(Team.applications)).limit(5).offset(0))
    teams_with_applications = result.scalars().unique().all()

    team_ids = [t.id for t in teams_with_applications]
    assert team_ids == [1, 2, 3, 4, 5]


async def test_one_to_many_eagerloading_is_good_with_pagination(test_db_session):
    """
    SELECT teams.id, teams.squad_name, teams.squad_lead, teams.tribe, teams.tribe_lead, teams.product_line, teams.dh_slack_group
    FROM teams
    LIMIT ? OFFSET ?
    SELECT applications.team_id AS applications_team_id, applications.id AS applications_id, applications.name AS applications_name, applications.description AS applications_description
    FROM applications
    WHERE applications.team_id IN (?, ?, ?, ?, ?)
    """
    async with test_db_session.begin():
        teams = []
        for i in range(1, 10):
            team = Team(
                squad_name=f"Test Squad_{i}",
                squad_lead="Test Lead",
                tribe="Test Tribe",
                tribe_lead="Test Tribe Lead",
                product_line="Test Product",
                dh_slack_group="test-slack",
            )
            team.applications.append(Application(name=f"application_{i}_1"))
            team.applications.append(Application(name=f"application_{i}_2"))
            teams.append(team)
        test_db_session.add_all(teams)

    result = await test_db_session.execute(select(Team).limit(5).offset(0).options(selectinload(Team.applications)))
    teams_with_applications = result.scalars().all()

    team_ids = [t.id for t in teams_with_applications]
    assert team_ids == [1, 2, 3, 4, 5]
