from sqlalchemy import BOOLEAN, Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import expression

from app.db import DeclarativeBase


class BaseId(DeclarativeBase):
    __abstract__ = True
    __tablename__ = None

    _id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.uuid6(),
        name="id",
        doc=f"Unique index of {__tablename__}",
    )
    is_active = Column(
        BOOLEAN,
        server_default=expression.true(),
        nullable=False,
        doc="Is active.",
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="DateTime of creation",
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="DateTime of changes",
    )
