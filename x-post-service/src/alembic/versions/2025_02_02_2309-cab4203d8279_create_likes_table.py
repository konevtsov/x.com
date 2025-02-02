"""Create likes table

Revision ID: cab4203d8279
Revises: b1c3696fea3b
Create Date: 2025-02-02 23:09:37.133992

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cab4203d8279"
down_revision: Union[str, None] = "b1c3696fea3b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "likes",
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"], ["posts.id"], name=op.f("fk_likes_post_id_posts")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_likes")),
        sa.UniqueConstraint("post_id", "user_id", name="unique_like"),
    )


def downgrade() -> None:
    op.drop_table("likes")
