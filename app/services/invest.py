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
) -> None:
    """Инвестирует свободные донаты в открытые проекты."""
    projects = await charity_project_crud.get_multi_with_free_amount(session)
    donations = await donation_crud.get_multi_with_free_amount(session)

    project_index, projects_len = 0, len(projects)
    donation_index, donations_len = 0, len(donations)

    changed_objs = set()

    while donation_index < donations_len and project_index < projects_len:
        project = projects[project_index]
        donation = donations[donation_index]

        project_free_amount = project.full_amount - project.invested_amount
        donation_free_amount = donation.full_amount - donation.invested_amount

        if donation_free_amount >= project_free_amount:
            donation.invested_amount += project_free_amount
            project.invested_amount += project_free_amount

            close_obj(project)
            close_obj(donation)

            project_index += 1

            if donation.fully_invested:
                donation_index += 1

        else:
            donation.invested_amount += donation_free_amount
            project.invested_amount += donation_free_amount

            close_obj(donation)

            donation_index += 1

        changed_objs.update({project, donation})

    session.add_all(changed_objs)
    await session.commit()
