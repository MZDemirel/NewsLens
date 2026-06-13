"""initial_tables

Revision ID: c75c76105e9c
Revises: 
Create Date: 2026-06-13 15:59:31.086443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c75c76105e9c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "news",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text()),
        sa.Column("full_text", sa.Text()),
        sa.Column("url", sa.Text(), nullable=False, unique=True),
        sa.Column("category", sa.String(50)),
        sa.Column("published_at", sa.DateTime()),
        sa.Column("fetched_at", sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        "user_interactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("news_id", sa.Integer(), sa.ForeignKey("news.id"), nullable=False),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("dwell_time_sec", sa.Integer()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("user_interactions")
    op.drop_table("news")
    op.drop_table("users")
