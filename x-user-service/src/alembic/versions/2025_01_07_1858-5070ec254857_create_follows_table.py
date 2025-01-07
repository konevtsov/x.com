"""Create follows table

Revision ID: 5070ec254857
Revises: 6320b580d78d
Create Date: 2025-01-07 18:58:12.852192

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5070ec254857"
down_revision: Union[str, None] = "6320b580d78d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "follows",
        sa.Column("followed_id", sa.Integer(), nullable=False),
        sa.Column("follower_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["followed_id"],
            ["users.id"],
            name=op.f("fk_follows_followed_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["follower_id"],
            ["users.id"],
            name=op.f("fk_follows_follower_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_follows")),
        sa.UniqueConstraint(
            "followed_id", "follower_id", name="unique_follow"
        ),
    )


def downgrade() -> None:
    op.drop_table("follows")
