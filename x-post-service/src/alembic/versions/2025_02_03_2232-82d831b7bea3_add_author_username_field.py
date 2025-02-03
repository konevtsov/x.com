"""Add author_username field

Revision ID: 82d831b7bea3
Revises: cab4203d8279
Create Date: 2025-02-03 22:32:19.551818

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "82d831b7bea3"
down_revision: Union[str, None] = "cab4203d8279"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts", sa.Column("author_username", sa.String(), nullable=False)
    )
    op.drop_constraint("uq_posts_user_id", "posts", type_="unique")


def downgrade() -> None:
    op.create_unique_constraint("uq_posts_user_id", "posts", ["user_id"])
    op.drop_column("posts", "author_username")
