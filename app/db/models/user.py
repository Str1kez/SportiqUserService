from sqlalchemy import VARCHAR
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import BaseId


class User(BaseId):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(
        VARCHAR(30),
        nullable=False,
        unique=True,
        index=True,
    )
    password: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(
        VARCHAR(30),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        VARCHAR(30),
        nullable=False,
    )
