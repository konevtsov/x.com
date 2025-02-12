"""Add avatar_url field

Revision ID: 9555897e8e22
Revises: c7de81a7c0e8
Create Date: 2025-02-11 23:55:46.992289

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9555897e8e22"
down_revision: Union[str, None] = "c7de81a7c0e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("avatar_url", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "avatar_url")
