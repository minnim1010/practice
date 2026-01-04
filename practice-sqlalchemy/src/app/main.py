import asyncio
import time
from pprint import pprint

from app.application.dto import ApplicationCreate, ApplicationUpdate
from app.application.service import (
    add_application,
    get_applications,
    update_application,
    get_application,
    delete_application,
)
from app.team.dto import TeamCreate
from app.team.service import add_team


async def main():
    # await create_tables(drop=True)
    team_create_data = TeamCreate(
        squad_name="Test Squad",
        squad_lead="Test Lead",
        tribe="Test Tribe",
        tribe_lead="Test Tribe Lead",
        product_line="Test Product",
        dh_slack_group="test-slack",
    )
    team = await add_team(team_create_data)
    pprint(team)

    application_values = ApplicationCreate(name=f"application_{time.time()}", team_id=team.id)
    await add_application(application_values)

    applications = await get_applications()
    pprint(applications)

    application = applications[0]
    update_application_values = ApplicationUpdate(
        name=f"update_application_{time.time()}", description="update", team_id=application.team_id
    )
    await update_application(application.id, update_application_values)
    updated_application = await get_application(application.id)
    pprint(updated_application)

    await delete_application(updated_application.id)
    applications = await get_applications()
    pprint(applications)


if __name__ == "__main__":
    asyncio.run(main())
