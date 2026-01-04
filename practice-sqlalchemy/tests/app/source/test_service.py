import pytest
import pytest_asyncio
from app.source.service import (
    add_source,
    get_sources,
    get_source,
    update_source,
    delete_source,
)
from app.source.dto import SourceCreate, SourceUpdate


@pytest_asyncio.fixture(autouse=True)
def override_db_session(monkeypatch, test_db_session):
    """
    Fixture to automatically replace AsyncSessionLocal with the test database session.
    """
    monkeypatch.setattr(
        "app.source.service.AsyncSessionLocal",
        lambda: test_db_session,
    )


async def test_add_source():
    source_create_data = SourceCreate(name="Test Source")

    created_source = await add_source(source_create_data)

    assert created_source.id is not None
    assert created_source.name == "Test Source"

    retrieved_source = await get_source(created_source.id)
    assert retrieved_source.name == "Test Source"


async def test_get_sources():
    source1_data = SourceCreate(name="Source 1")
    source2_data = SourceCreate(name="Source 2")
    await add_source(source1_data)
    await add_source(source2_data)

    sources = await get_sources()

    assert len(sources) == 2
    assert sources[0].name == "Source 1"
    assert sources[1].name == "Source 2"


async def test_get_source():
    source_data = SourceCreate(name="Test Source")
    created_source = await add_source(source_data)

    retrieved_source = await get_source(created_source.id)

    assert retrieved_source is not None
    assert retrieved_source.id == created_source.id
    assert retrieved_source.name == "Test Source"


async def test_get_source_not_found():
    with pytest.raises(ValueError, match="Source with id 999 not found."):
        await get_source(999)


async def test_update_source():
    source_data = SourceCreate(name="Old Source Name")
    created_source = await add_source(source_data)
    update_data = SourceUpdate(name="New Source Name")

    await update_source(source_id=created_source.id, source_values=update_data)

    updated_source = await get_source(created_source.id)
    assert updated_source.name == "New Source Name"


async def test_delete_source():
    source_data = SourceCreate(name="Source to Delete")
    created_source = await add_source(source_data)

    await delete_source(created_source.id)

    with pytest.raises(ValueError):
        await get_source(created_source.id)
