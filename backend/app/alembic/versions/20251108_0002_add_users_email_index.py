"""add explicit users(email) index to align with SQL script

Revision ID: 20251108_0002
Revises: 20251107_0001
Create Date: 2025-11-08

"""
from typing import Sequence, Union
from alembic import op

revision: str = "20251108_0002"
down_revision: Union[str, None] = "20251107_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("idx_users_email", "users", ["email"], unique=False)


def downgrade() -> None:
    op.drop_index("idx_users_email", table_name="users")
