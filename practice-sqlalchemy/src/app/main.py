import asyncio
import time
from pprint import pprint

from app.database import create_tables
from app.team.dto import TeamCreate, TeamUpdate
from app.team.service import add_team, get_teams, update_team, delete_team, get_team


async def main():
    await create_tables()
    team_values = TeamCreate(
        squad_name=f"squad_{time.time()}",
        squad_lead="example",
        tribe="example",
        tribe_lead="example",
        product_line="example",
        dh_slack_group="example",
    )
    await add_team(team_values)

    teams = await get_teams()
    pprint(teams)

    update_team_values = TeamUpdate(
        squad_name=f"update_squad_{time.time()}",
        squad_lead="update",
        tribe="update",
        tribe_lead="update",
        product_line="update",
        dh_slack_group="update",
    )
    await update_team(1, update_team_values)
    team = await get_team(1)
    pprint(team)

    await delete_team(2)
    teams = await get_teams()
    pprint(teams)


if __name__ == "__main__":
    asyncio.run(main())
