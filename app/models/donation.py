from sqlalchemy import Column, ForeignKey, String, Text

from app.models.investment import Investment


class Donation(Investment):
    user_id = Column(String, ForeignKey('user.id'))
    comment = Column(Text)
