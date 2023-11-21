"""add receiver, phone number, address and order by in transactions table

Revision ID: e66827776ec9
Revises: 13644f6ef3a3
Create Date: 2023-11-21 10:19:03.153529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e66827776ec9'
down_revision: Union[str, None] = '13644f6ef3a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('transaction_sf', sa.Column('receiver', sa.String(255), nullable=True))
    op.add_column('transaction_sf', sa.Column('phone_number', sa.String(255), nullable=True))
    op.add_column('transaction_sf', sa.Column('address', sa.String(255), nullable=True))
    op.add_column('transaction_sf', sa.Column('order_by', sa.String(255), nullable=True))
    op.add_column('transaction_fm', sa.Column('receiver', sa.String(255), nullable=True))
    op.add_column('transaction_fm', sa.Column('phone_number', sa.String(255), nullable=True))
    op.add_column('transaction_fm', sa.Column('address', sa.String(255), nullable=True))
    op.add_column('transaction_fm', sa.Column('order_by', sa.String(255), nullable=True))
    op.add_column('transaction_fm', sa.Column('is_choose', sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column('transaction_sf', 'receiver')
    op.drop_column('transaction_sf', 'phone_number')
    op.drop_column('transaction_sf', 'address')
    op.drop_column('transaction_sf', 'order_by')
    op.drop_column('transaction_fm', 'receiver')
    op.drop_column('transaction_fm', 'phone_number')
    op.drop_column('transaction_fm', 'address')
    op.drop_column('transaction_fm', 'order_by')
    op.drop_column('transaction_fm', 'is_choose')
