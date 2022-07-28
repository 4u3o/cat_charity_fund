from sqlalchemy import Column, String, Text

from app.models.investment import Investment


class CharityProject(Investment):
    name: str = Column(String(100), unique=True, nullable=False)
    description: str = Column(Text, nullable=False)
