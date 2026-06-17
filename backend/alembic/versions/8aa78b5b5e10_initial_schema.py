"""initial schema

Revision ID: 8aa78b5b5e10
Revises: 
Create Date: 2026-06-18 02:19:30.411679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8aa78b5b5e10'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "users",

        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("user_name", sa.String(100), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="customer")
    )

    op.create_table(
        "cart",

        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("item_name",sa.String(100),nullable=False,unique=True),
        sa.Column("quantity",sa.Integer(),nullable=False)
    )

    op.create_table(
        "products",

        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("product_name",sa.String(50),nullable=False),
        sa.Column("product_category",sa.String(40),nullable=False),
        sa.Column("price",sa.Numeric(),nullable=False),
        sa.Column("seller_id",sa.Integer(),nullable=False),
        sa.ForeignKeyConstraint(["seller_id"],["users.id"])
    )


def downgrade() -> None:
    # Always in reverse order 
    op.drop_table("products")

    op.drop_table("cart")

    op.drop_table("users")