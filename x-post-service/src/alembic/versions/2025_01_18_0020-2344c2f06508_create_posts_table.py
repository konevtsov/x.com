"""Create posts table

Revision ID: 2344c2f06508
Revises: 
Create Date: 2025-01-18 00:20:53.749771

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2344c2f06508"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("author_username", sa.String(length=32), nullable=False),
        sa.Column("author_email", sa.Text(), nullable=False),
        sa.Column("text", sa.String(length=280), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_posts")),
        sa.UniqueConstraint(
            "author_email", name=op.f("uq_posts_author_email")
        ),
        sa.UniqueConstraint(
            "author_username", name=op.f("uq_posts_author_username")
        ),
    )


def downgrade() -> None:
    op.drop_table("posts")
