"""add number of sales in product

Revision ID: ce577cf7efe3
Revises: 765ca31342b5
Create Date: 2023-10-21 13:54:13.567662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce577cf7efe3'
down_revision: Union[str, None] = '765ca31342b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('product', sa.Column('number_of_sales', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    op.drop_column('product', 'number_of_sales')
