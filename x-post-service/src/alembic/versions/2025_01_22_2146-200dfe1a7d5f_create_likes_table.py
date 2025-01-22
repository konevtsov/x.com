"""Create likes table

Revision ID: 200dfe1a7d5f
Revises: ee808bcce893
Create Date: 2025-01-22 21:46:25.289491

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "200dfe1a7d5f"
down_revision: Union[str, None] = "ee808bcce893"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "likes",
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("author_email", sa.Text(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_id"], ["posts.id"], name=op.f("fk_likes_post_id_posts")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_likes")),
        sa.UniqueConstraint("post_id", "author_email", name="unique_like"),
    )


def downgrade() -> None:
    op.drop_table("likes")
