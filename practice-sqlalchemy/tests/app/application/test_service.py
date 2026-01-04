import pytest
import pytest_asyncio
from app.application.service import (
    add_application,
    get_applications,
    get_application,
    update_application,
    delete_application,
)
from app.application.dto import ApplicationCreate, ApplicationUpdate


@pytest_asyncio.fixture(autouse=True)
def override_db_session(monkeypatch, test_db_session):
    """
    Fixture to automatically replace AsyncSessionLocal with the test database session.
    """
    monkeypatch.setattr(
        "app.application.service.AsyncSessionLocal",
        lambda: test_db_session,
    )


async def test_add_application(seed_teams):
    application_create_data = ApplicationCreate(
        name="Test Application",
        description="A test application.",
        team_id=1,
    )

    created_application = await add_application(application_create_data)

    assert created_application.id is not None
    assert created_application.name == "Test Application"

    retrieved_application = await get_application(created_application.id)
    assert retrieved_application.name == "Test Application"


async def test_get_applications(seed_teams):
    app1_data = ApplicationCreate(name="Application 1", description="First app", team_id=1)
    app2_data = ApplicationCreate(name="Application 2", description="Second app", team_id=2)
    await add_application(app1_data)
    await add_application(app2_data)

    applications = await get_applications()

    assert len(applications) == 2
    assert applications[0].name == "Application 1"
    assert applications[1].name == "Application 2"


async def test_get_application(seed_teams):
    app_data = ApplicationCreate(name="Test Application", description="A test app", team_id=1)
    created_application = await add_application(app_data)

    retrieved_application = await get_application(created_application.id)

    assert retrieved_application is not None
    assert retrieved_application.id == created_application.id
    assert retrieved_application.name == "Test Application"


async def test_get_application_not_found(seed_teams):
    with pytest.raises(ValueError, match="application with id 999 not found."):
        await get_application(999)


async def test_update_application(seed_teams):
    app_data = ApplicationCreate(name="Old Application Name", description="Old description", team_id=1)
    created_application = await add_application(app_data)
    update_data = ApplicationUpdate(name="New Application Name", description="New description", team_id=1)

    await update_application(application_id=created_application.id, application_values=update_data)

    updated_application = await get_application(created_application.id)
    assert updated_application.name == "New Application Name"


async def test_delete_application(seed_teams):
    app_data = ApplicationCreate(name="App to Delete", description="This will be deleted", team_id=1)
    created_application = await add_application(app_data)

    await delete_application(created_application.id)

    with pytest.raises(ValueError):
        await get_application(created_application.id)
