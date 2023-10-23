"""add qr code and transaction code in user table

Revision ID: 6408ab66eb8a
Revises: ce577cf7efe3
Create Date: 2023-10-21 18:13:29.725532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6408ab66eb8a'
down_revision: Union[str, None] = 'ce577cf7efe3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('qr_code', sa.String(255), nullable=True))
    op.add_column('user', sa.Column('account_balance', sa.Float(), nullable=False, server_default='5.0'))


def downgrade() -> None:
    op.drop_column('user', 'qr_code')
    op.drop_column('user', 'account_balance')
