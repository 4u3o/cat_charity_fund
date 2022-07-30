from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject
from app.models.donation import Donation


def close_obj(obj: Union[Donation, CharityProject]) -> None:
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


async def start_invest(
    session: AsyncSession,
):
    """Инвестирует свободные донаты в открытые проекты.

    Args:
        session: AsyncSession.

    Returns:
        None.

    """
    projects = await charity_project_crud.get_multi_with_free_amount(session)
    donations = await donation_crud.get_multi_with_free_amount(session)

    project_index, projects_max_index = 0, len(projects) - 1
    donation_index, donations_max_index = 0, len(donations) - 1

    while not projects[project_index].fully_invested:
        project = projects[project_index]
        donation = donations[donation_index]

        project_free_amount = project.full_amount - project.invested_amount
        donation_free_amount = donation.full_amount - donation.invested_amount

        if donation_free_amount >= project_free_amount:
            donation.invested_amount += project_free_amount
            project.invested_amount += project_free_amount

            close_obj(project)
            close_obj(donation)

            if project_index < projects_max_index:
                project_index += 1

            if donation_index < donations_max_index:
                donation_index += 1

        else:
            donation.invested_amount += donation_free_amount
            project.invested_amount += donation_free_amount

            close_obj(donation)

            if donation_index < donations_max_index:
                donation_index += 1

    changed_objs = projects[:project_index + 1].extend(
        donations[:donation_index + 1]
    )
    await session.add_all(changed_objs)
    await session.commit()
