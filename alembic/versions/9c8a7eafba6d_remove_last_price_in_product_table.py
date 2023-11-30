"""remove last price in product table

Revision ID: 9c8a7eafba6d
Revises: 8531e54f09ef
Create Date: 2023-11-30 16:26:23.416208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c8a7eafba6d'
down_revision: Union[str, None] = '8531e54f09ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('product', 'last_price')


def downgrade() -> None:
    op.add_column('product', sa.Column('last_price', sa.Integer(), nullable=True, server_default='0'))
