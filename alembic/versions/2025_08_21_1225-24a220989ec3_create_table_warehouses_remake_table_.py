"""create table warehouses. remake table product_stocks.

Revision ID: 24a220989ec3
Revises: c34a81e11a86
Create Date: 2025-08-21 12:25:41.414704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24a220989ec3'
down_revision: Union[str, Sequence[str], None] = 'c34a81e11a86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'warehouses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('address', sa.String(length=200), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table(
        'product_stocks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('product_code', sa.String(length=20), nullable=False),
        sa.Column('warehouse_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('reserved', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.ForeignKeyConstraint(
            ['product_code'],
            ['products.code'],
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['warehouse_id'],
            ['warehouses.id'],
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('product_code', 'warehouse_id', name='uq_product_warehouse')
    )

    op.create_index('ix_product_stocks_product_code', 'product_stocks', ['product_code'])
    op.create_index('ix_product_stocks_warehouse_id', 'product_stocks', ['warehouse_id'])


def downgrade():
    op.drop_table('product_stocks')
    op.drop_table('warehouses')
