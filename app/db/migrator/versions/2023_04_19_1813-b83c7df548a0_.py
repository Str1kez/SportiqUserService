"""empty message

Revision ID: b83c7df548a0
Revises: e5a927bdb33c
Create Date: 2023-04-19 18:13:50.244094

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "b83c7df548a0"
down_revision = "e5a927bdb33c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("phone_number", sa.VARCHAR(length=20), nullable=False))
    op.create_index(op.f("ix__user__phone_number"), "user", ["phone_number"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix__user__phone_number"), table_name="user")
    op.drop_column("user", "phone_number")
