"""Create posts table

Revision ID: ee808bcce893
Revises: 
Create Date: 2025-01-18 23:45:13.670901

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ee808bcce893"
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
    )


def downgrade() -> None:
    op.drop_table("posts")
