"""remove transaction code in financial transaction table

Revision ID: 67f1cd766b32
Revises: 1f8cf532d39b
Create Date: 2023-11-28 14:19:50.045835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67f1cd766b32'
down_revision: Union[str, None] = '1f8cf532d39b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('financial_transaction', 'transaction_code')


def downgrade() -> None:
    op.add_column('financial_transaction', sa.Column('transaction_code', sa.String(255), nullable=False))
