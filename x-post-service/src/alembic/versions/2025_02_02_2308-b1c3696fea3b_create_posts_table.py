"""Create posts table

Revision ID: b1c3696fea3b
Revises: 
Create Date: 2025-02-02 23:08:20.916826

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1c3696fea3b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=280), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_posts")),
        sa.UniqueConstraint("user_id", name=op.f("uq_posts_user_id")),
    )


def downgrade() -> None:
    op.drop_table("posts")
