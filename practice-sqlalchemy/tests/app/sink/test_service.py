import pytest
import pytest_asyncio
from app.sink.service import (
    add_sink,
    get_sinks,
    get_sink,
    update_sink,
    delete_sink,
)
from app.sink.dto import SinkCreate, SinkUpdate


@pytest_asyncio.fixture(autouse=True)
def override_db_session(monkeypatch, test_db_session):
    """
    Fixture to automatically replace AsyncSessionLocal with the test database session.
    """
    monkeypatch.setattr(
        "app.sink.service.AsyncSessionLocal",
        lambda: test_db_session,
    )


async def test_add_sink():
    sink_create_data = SinkCreate(name="Test Sink")

    created_sink = await add_sink(sink_create_data)

    assert created_sink.id is not None
    assert created_sink.name == "Test Sink"

    retrieved_sink = await get_sink(created_sink.id)
    assert retrieved_sink.name == "Test Sink"


async def test_get_sinks():
    sink1_data = SinkCreate(name="Sink 1")
    sink2_data = SinkCreate(name="Sink 2")
    await add_sink(sink1_data)
    await add_sink(sink2_data)

    sinks = await get_sinks()

    assert len(sinks) == 2
    assert sinks[0].name == "Sink 1"
    assert sinks[1].name == "Sink 2"


async def test_get_sink():
    sink_data = SinkCreate(name="Test Sink")
    created_sink = await add_sink(sink_data)

    retrieved_sink = await get_sink(created_sink.id)

    assert retrieved_sink is not None
    assert retrieved_sink.id == created_sink.id
    assert retrieved_sink.name == "Test Sink"


async def test_get_sink_not_found():
    with pytest.raises(ValueError, match="Sink with id 999 not found."):
        await get_sink(999)


async def test_update_sink():
    sink_data = SinkCreate(name="Old Sink Name")
    created_sink = await add_sink(sink_data)
    update_data = SinkUpdate(name="New Sink Name")

    await update_sink(sink_id=created_sink.id, sink_values=update_data)

    updated_sink = await get_sink(created_sink.id)
    assert updated_sink.name == "New Sink Name"


async def test_delete_sink():
    sink_data = SinkCreate(name="Sink to Delete")
    created_sink = await add_sink(sink_data)

    await delete_sink(created_sink.id)

    with pytest.raises(ValueError):
        await get_sink(created_sink.id)
