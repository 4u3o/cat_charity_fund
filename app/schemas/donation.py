from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel, Extra, Field, PositiveInt
)


class DonationBase(BaseModel):
    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationDBShort(DonationCreate):
    id: int
    create_date: datetime


class DonationDBFull(DonationDBShort):
    user_id: UUID
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
