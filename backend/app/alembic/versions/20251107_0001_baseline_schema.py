"""baseline schema

Revision ID: 20251107_0001
Revises: 
Create Date: 2025-11-07

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "20251107_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	# users
	op.create_table(
		"users",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("email", sa.String(length=255), nullable=False, unique=True, index=True),
		sa.Column("hashed_password", sa.String(length=255), nullable=False),
		sa.Column("full_name", sa.String(length=255)),
		sa.Column("phone_number", sa.String(length=20)),
		sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
	)

	# categories
	op.create_table(
		"categories",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("name", sa.String(length=100), nullable=False),
		sa.Column("icon_url", sa.String(length=255)),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
	)

	# products
	op.create_table(
		"products",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id")),
		sa.Column("name", sa.String(length=255), nullable=False),
		sa.Column("description", sa.Text()),
		sa.Column("price", sa.Numeric(10, 2), nullable=False),
		sa.Column("image_url", sa.String(length=255)),
		sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.text("1")),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
	)
	op.create_index("idx_products_category_id", "products", ["category_id"])

	# locations
	op.create_table(
		"locations",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
		sa.Column("name", sa.String(length=100), nullable=False),
		sa.Column("address", sa.Text(), nullable=False),
		sa.Column("latitude", sa.Numeric(10, 8)),
		sa.Column("longitude", sa.Numeric(11, 8)),
		sa.Column("is_favorite", sa.Boolean(), nullable=False, server_default=sa.text("0")),
	)

	# orders
	order_status_enum = sa.Enum(
		"PENDING",
		"CONFIRMED",
		"PREPARING",
		"ON_THE_WAY",
		"DELIVERED",
		"CANCELLED",
		name="order_status",
	)
	op.create_table(
		"orders",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
		sa.Column("status", order_status_enum, nullable=False, server_default="PENDING"),
		sa.Column("total_amount", sa.Numeric(10, 2), nullable=False),
		sa.Column("delivery_address", sa.Text()),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
		sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
	)
	op.create_index("idx_orders_user_id", "orders", ["user_id"])
	op.create_index("idx_orders_status", "orders", ["status"])

	# order_items
	op.create_table(
		"order_items",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id", ondelete="CASCADE")),
		sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id")),
		sa.Column("quantity", sa.Integer(), nullable=False),
		sa.Column("price_at_time", sa.Numeric(10, 2), nullable=False),
	)

	# drivers
	op.create_table(
		"drivers",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
		sa.Column("license_plate", sa.String(length=20)),
		sa.Column("vehicle_type", sa.String(length=50)),
		sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.text("1")),
	)

	# payments
	payment_method_enum = sa.Enum("CASH", "CARD", "QRIS", name="payment_method")
	payment_status_enum = sa.Enum("PENDING", "SUCCESS", "FAILED", name="payment_status")
	op.create_table(
		"payments",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id", ondelete="CASCADE")),
		sa.Column("method", payment_method_enum, nullable=False),
		sa.Column("status", payment_status_enum, nullable=False, server_default="PENDING"),
		sa.Column("transaction_id", sa.String(length=255)),
	)

	# reviews
	op.create_table(
		"reviews",
		sa.Column("id", sa.Integer(), primary_key=True),
		sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
		sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id")),
		sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id")),
		sa.Column("driver_id", sa.Integer(), sa.ForeignKey("drivers.id")),
		sa.Column("rating", sa.Integer(), nullable=False),
		sa.Column("comment", sa.Text()),
		sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
		sa.CheckConstraint("rating >= 1 AND rating <= 5", name="ck_reviews_rating_range"),
	)


def downgrade() -> None:
	op.drop_table("reviews")
	op.drop_table("payments")
	op.drop_table("drivers")
	op.drop_table("order_items")
	op.drop_index("idx_orders_status", table_name="orders")
	op.drop_index("idx_orders_user_id", table_name="orders")
	op.drop_table("orders")
	op.drop_table("locations")
	op.drop_index("idx_products_category_id", table_name="products")
	op.drop_table("products")
	op.drop_table("categories")
	op.drop_table("users")
	# Drop enums explicitly (MySQL may require manual cleanup depending on dialect)
	# (No action needed for MySQL enum cleanup by Alembic normally.)