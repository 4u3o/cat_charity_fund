from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, Extra, Field, PositiveInt
)


class CharityProjectBase(BaseModel):
    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(..., max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectDB(CharityProjectCreate):
    id: str
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
