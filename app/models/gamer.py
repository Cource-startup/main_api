from sqlalchemy import Column, ForeignKey, Identity, Integer
from datetime import datetime
from .user import User
from db import db

class Gamer(User):
    __tablename__ = 'gamers'
    __mapper_args__ = {
        'polymorphic_identity': 'gamers',
    }

    mutable_fields = [
        "first_name",
        "last_name",
        "nickname",
        "avatar",
        "best_score",
    ]

    id = Column(None, ForeignKey('users.id'), primary_key=True)
    best_score = Column(Integer, nullable=False, default=0)
