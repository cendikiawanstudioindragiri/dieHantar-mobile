"""add unique constraint on categories.name

Revision ID: 20251108_0004
Revises: 20251108_0003
Create Date: 2025-11-08
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251108_0004'
down_revision = '20251108_0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('categories') as batch_op:
        batch_op.create_unique_constraint('uq_categories_name', ['name'])


def downgrade() -> None:
    with op.batch_alter_table('categories') as batch_op:
        batch_op.drop_constraint('uq_categories_name', type_='unique')
