"""Add user_id field

Revision ID: c7de81a7c0e8
Revises: 5070ec254857
Create Date: 2025-02-02 22:34:37.140065

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c7de81a7c0e8"
down_revision: Union[str, None] = "5070ec254857"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_unique_constraint(op.f("uq_users_user_id"), "users", ["user_id"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_users_user_id"), "users", type_="unique")
    op.drop_column("users", "user_id")
