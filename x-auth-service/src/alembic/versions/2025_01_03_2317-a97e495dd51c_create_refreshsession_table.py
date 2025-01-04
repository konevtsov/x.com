"""Create RefreshSession table

Revision ID: a97e495dd51c
Revises: 610c15941ce5
Create Date: 2025-01-03 23:17:35.642098

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a97e495dd51c"
down_revision: Union[str, None] = "610c15941ce5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_sessions",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "refresh_token_uuid", sa.Uuid(as_uuid=False), nullable=False
        ),
        sa.Column("refresh_token", sa.Text(), nullable=False),
        sa.Column("ip", sa.String(length=16), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_refresh_sessions_user_id_users"),
            ondelete="CASCADE",  # !Added manually
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_sessions")),
    )
    op.drop_column("users", "refresh_token")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "refresh_token", sa.TEXT(), autoincrement=False, nullable=True
        ),
    )
    op.drop_table("refresh_sessions")
