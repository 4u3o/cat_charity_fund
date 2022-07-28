from sqlalchemy import Column, DateTime, Boolean, Integer
from sqlalchemy.sql import func

from app.core.db import Base


class Investment(Base):
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, server_default=func.now())
    close_date = Column(DateTime)
