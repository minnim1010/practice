from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.source.dto import SourceCreate, SourceRead, SourceUpdate
from app.source.model import Source
from app.database import AsyncSessionLocal


async def add_source(source_values: SourceCreate) -> SourceRead:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_source = Source(**source_values.model_dump())
            session.add(new_source)
        await session.refresh(new_source)
        return SourceRead.model_validate(new_source)


async def get_sources() -> list[SourceRead]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Source))
        sources = result.scalars().all()
        return [SourceRead.model_validate(s) for s in sources]


async def get_source(source_id: int) -> SourceRead:
    async with AsyncSessionLocal() as session:
        source = await _get_source(session, source_id)
        return SourceRead.model_validate(source)


async def update_source(source_id: int, source_values: SourceUpdate):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            source = await _get_source(session, source_id)
            for key, value in source_values.model_dump().items():
                setattr(source, key, value)


async def delete_source(source_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            source = await _get_source(session, source_id)
            await session.delete(source)


async def _get_source(session: AsyncSession, source_id: int) -> Source:
    result = await session.execute(select(Source).filter(Source.id == source_id))
    source = result.scalar_one_or_none()
    if source is None:
        raise ValueError(f"Source with id {source_id} not found.")
    return source
