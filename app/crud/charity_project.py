from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate
)


class CRUDCharityProject(
    CRUDBase[
        CharityProject,
        CharityProjectCreate,
        CharityProjectUpdate
    ]
):
    async def get(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        project_result = await session.execute(
            select(CharityProject).where(CharityProject.id == project_id)
        )

        return project_result.scalars().first()

    async def get_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        project_result = await session.execute(
            select(CharityProject).where(CharityProject.name == project_name)
        )

        return project_result.scalars().first()

    async def remove(
        self,
        project: CharityProject,
        session: AsyncSession,
    ) -> None:
        await session.delete(project)
        await session.commit()


charity_project_crud = CRUDCharityProject(CharityProject)
