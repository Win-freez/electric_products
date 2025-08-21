"""add_created_at_to_warehouses

Revision ID: 11d21a715170
Revises: 24a220989ec3
Create Date: 2025-08-21 14:21:19.154654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '11d21a715170'
down_revision: Union[str, Sequence[str], None] = '24a220989ec3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('warehouses', sa.Column('created_at', sa.DateTime(), nullable=True))
    # Заполнить существующие записи
    op.execute("UPDATE warehouses SET created_at = NOW()")
    op.alter_column('warehouses', 'created_at', nullable=False)


def downgrade():
    op.drop_column('warehouses', 'created_at')
