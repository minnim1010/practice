from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.application.dto import ApplicationCreate, ApplicationRead, ApplicationUpdate
from app.application.model import Application
from app.database import AsyncSessionLocal


async def add_application(application_values: ApplicationCreate) -> ApplicationRead:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_application = Application(**application_values.model_dump())
            session.add(new_application)
        await session.refresh(new_application)
        return ApplicationRead.model_validate(new_application)


async def get_applications() -> list[ApplicationRead]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Application))
        applications = result.scalars().all()
        return [ApplicationRead.model_validate(t) for t in applications]


async def get_application(application_id: int) -> ApplicationRead:
    async with AsyncSessionLocal() as session:
        application = await _get_application(session, application_id)
        return ApplicationRead.model_validate(application)


async def update_application(application_id: int, application_values: ApplicationUpdate):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            application = await _get_application(session, application_id)
            for key, value in application_values.model_dump().items():
                setattr(application, key, value)


async def delete_application(application_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            application = await _get_application(session, application_id)
            await session.delete(application)


async def _get_application(session: AsyncSession, application_id: int) -> Application:
    result = await session.execute(select(Application).filter(Application.id == application_id))
    application = result.scalar_one_or_none()
    if application is None:
        raise ValueError(f"application with id {application_id} not found.")
    return application
