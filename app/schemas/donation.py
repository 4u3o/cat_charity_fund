from datetime import datetime
from typing import Optional
# from uuid import UUID

from pydantic import (
    BaseModel, Extra, PositiveInt
)


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    class Config:
        extra = Extra.forbid


class DonationUpdate(DonationCreate):
    invested_amount: int
    fully_invested: Optional[bool]
    close_date: Optional[datetime]


class DonationDBShort(DonationBase):
    id: int
    create_date: datetime


class DonationDBFull(DonationDBShort):
    # убрал UUID чтобы пример был как в доке
    user_id: str
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
