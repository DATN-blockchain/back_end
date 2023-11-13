"""change name from  hash data to tx hash in the tables

Revision ID: 5e354ee8f0a6
Revises: 767a955387c2
Create Date: 2023-11-13 20:33:50.587893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e354ee8f0a6'
down_revision: Union[str, None] = '767a955387c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('user', 'hashed_data')
    op.drop_column('product', 'hashed_data')
    op.drop_column('grow_up', 'hashed_data')
    op.drop_column('marketplace', 'hashed_data')
    op.drop_column('transaction_sf', 'hashed_data')
    op.drop_column('transaction_fm', 'hashed_data')
    op.add_column('user', sa.Column('tx_hash', sa.Text(), nullable=True))
    op.add_column('product', sa.Column('tx_hash', sa.Text(), nullable=True))
    op.add_column('grow_up', sa.Column('tx_hash', sa.Text(), nullable=True))
    op.add_column('marketplace', sa.Column('tx_hash', sa.Text(), nullable=True))
    op.add_column('transaction_sf', sa.Column('tx_hash', sa.Text(), nullable=True))
    op.add_column('transaction_fm', sa.Column('tx_hash', sa.Text(), nullable=True))
    op.add_column('financial_transaction', sa.Column('tx_hash', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'tx_hash')
    op.drop_column('product', 'tx_hash')
    op.drop_column('grow_up', 'tx_hash')
    op.drop_column('marketplace', 'tx_hash')
    op.drop_column('transaction_sf', 'tx_hash')
    op.drop_column('transaction_fm', 'tx_hash')
    op.drop_column('financial_transaction', 'tx_hash')
    op.add_column('user', sa.Column('hashed_data', sa.String(255), nullable=True))
    op.add_column('product', sa.Column('hashed_data', sa.String(255), nullable=True))
    op.add_column('grow_up', sa.Column('hashed_data', sa.String(255), nullable=True))
    op.add_column('marketplace', sa.Column('hashed_data', sa.String(255), nullable=True))
    op.add_column('transaction_sf', sa.Column('hashed_data', sa.String(255), nullable=True))
    op.add_column('transaction_fm', sa.Column('hashed_data', sa.String(255), nullable=True))
