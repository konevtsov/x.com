"""Change name and bio fields nullable rule

Revision ID: 6320b580d78d
Revises: 5eabcca84a38
Create Date: 2024-12-12 22:38:52.198023

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6320b580d78d"
down_revision: Union[str, None] = "5eabcca84a38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users", "name", existing_type=sa.VARCHAR(length=50), nullable=True
    )
    op.alter_column(
        "users", "bio", existing_type=sa.VARCHAR(length=160), nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "users", "bio", existing_type=sa.VARCHAR(length=160), nullable=False
    )
    op.alter_column(
        "users", "name", existing_type=sa.VARCHAR(length=50), nullable=False
    )
