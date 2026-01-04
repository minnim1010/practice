from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import AsyncSessionLocal
from app.team.dto import TeamCreate, TeamRead, TeamUpdate
from app.team.model import Team


async def add_team(team_values: TeamCreate) -> TeamRead:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            new_team = Team(**team_values.model_dump())
            session.add(new_team)
        await session.refresh(new_team)
        return TeamRead.model_validate(new_team)


async def get_teams() -> list[TeamRead]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Team))
        teams = result.scalars().all()
        return [TeamRead.model_validate(t) for t in teams]


async def get_team(team_id: int) -> TeamRead:
    async with AsyncSessionLocal() as session:
        team = await _get_team(session, team_id)
        return TeamRead.model_validate(team)


async def update_team(team_id: int, team_values: TeamUpdate):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            team = await _get_team(session, team_id)
            for key, value in team_values.model_dump().items():
                setattr(team, key, value)


async def delete_team(team_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            team = await _get_team(session, team_id)
            await session.delete(team)


async def _get_team(session: AsyncSession, team_id: int) -> Team | None:
    result = await session.execute(select(Team).filter(Team.id == team_id))
    team = result.scalar_one_or_none()
    if team is None:
        raise ValueError(f"Team with id {team_id} not found.")
    return team
