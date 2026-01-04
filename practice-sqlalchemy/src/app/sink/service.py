from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.sink.dto import SinkCreate, SinkRead, SinkUpdate
from app.sink.model import Sink
from app.database import AsyncSessionLocal


async def add_sink(sink_values: SinkCreate) -> SinkRead:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_sink = Sink(**sink_values.model_dump())
            session.add(new_sink)
        await session.refresh(new_sink)
        return SinkRead.model_validate(new_sink)


async def get_sinks() -> list[SinkRead]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Sink))
        sinks = result.scalars().all()
        return [SinkRead.model_validate(s) for s in sinks]


async def get_sink(sink_id: int) -> SinkRead:
    async with AsyncSessionLocal() as session:
        sink = await _get_sink(session, sink_id)
        return SinkRead.model_validate(sink)


async def update_sink(sink_id: int, sink_values: SinkUpdate):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            sink = await _get_sink(session, sink_id)
            for key, value in sink_values.model_dump().items():
                setattr(sink, key, value)


async def delete_sink(sink_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            sink = await _get_sink(session, sink_id)
            await session.delete(sink)


async def _get_sink(session: AsyncSession, sink_id: int) -> Sink:
    result = await session.execute(select(Sink).filter(Sink.id == sink_id))
    sink = result.scalar_one_or_none()
    if sink is None:
        raise ValueError(f"Sink with id {sink_id} not found.")
    return sink
