from sqlalchemy import VARCHAR, Column
from sqlalchemy.dialects.postgresql import TEXT

from app.db.models.base import BaseId


class User(BaseId):
    __tablename__ = "user"

    username = Column(
        VARCHAR(30),
        nullable=False,
        unique=True,
        index=True,
    )
    password = Column(
        TEXT,
        nullable=False,
    )
    first_name = Column(
        VARCHAR(30),
        nullable=False,
    )
    last_name = Column(
        VARCHAR(30),
        nullable=False,
    )
