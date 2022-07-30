from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(
    CRUDBase[
        Donation,
        DonationCreate,
        DonationUpdate
    ]
):
    async def get_user_donations(
        self,
        session: AsyncSession,
        user: User,
    ) -> List[Donation]:
        donations_result = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations_result.scalars().all()


donation_crud = CRUDDonation(Donation)
