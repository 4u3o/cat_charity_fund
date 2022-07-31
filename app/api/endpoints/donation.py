from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationDBFull, DonationDBShort
)
from app.services.invest import start_invest


router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDBFull],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.

    Получает список всех пожертвований.
    """
    donations = await donation_crud.get_multi(session)

    return donations


@router.post(
    '/',
    response_model=DonationDBShort,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    donation = await donation_crud.create(
        donation, session, user
    )

    if await charity_project_crud.is_not_fully_invested(session):
        await start_invest(session)
        await session.refresh(donation)

    return donation


@router.get(
    '/my',
    response_model=List[DonationDBShort],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получить список моих пожертвований."""
    donations = await donation_crud.get_user_donations(session, user)

    return donations
