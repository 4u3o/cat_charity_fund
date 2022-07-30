from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_not_invested(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)

    if project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='На данный проект уже поступили пожертвования.'
        )

    return project


async def check_project_not_closed(
    project_id: int,
    session: AsyncSession,
):
    project = await charity_project_crud.get(project_id, session)

    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Данный проект закрыт, редактировать нельзя.'
        )


async def check_full_amount_gt_invested(
    project: CharityProject,
    full_amount: int,
):
    if project.invested_amount > full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя установить требуемую сумму меньше уже вложенной.'
        )
