"""add last price in product table

Revision ID: d4ff1dad4f72
Revises: b83909941949
Create Date: 2023-11-18 15:59:17.004584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.


revision: str = 'd4ff1dad4f72'
down_revision: Union[str, None] = 'b83909941949'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('product', sa.Column('last_price', sa.Integer(), nullable=True, server_default='0'))


def downgrade() -> None:
    op.drop_column('product', 'last_price')
