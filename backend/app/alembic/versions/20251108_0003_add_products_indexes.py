"""add product indexes for common filters

Revision ID: 20251108_0003
Revises: 20251108_0002
Create Date: 2025-11-08

"""
from typing import Sequence, Union
from alembic import op

revision: str = "20251108_0003"
down_revision: Union[str, None] = "20251108_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Individual index for availability filter
    op.create_index("idx_products_is_available", "products", ["is_available"], unique=False)
    # Composite index for category + availability + created_at (sorting)
    op.create_index(
        "idx_products_category_avail_created",
        "products",
        ["category_id", "is_available", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_products_category_avail_created", table_name="products")
    op.drop_index("idx_products_is_available", table_name="products")
