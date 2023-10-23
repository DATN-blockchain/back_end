"""create financial transaction table

Revision ID: 76b958e8203b
Revises: 6408ab66eb8a
Create Date: 2023-10-21 23:58:58.883801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '76b958e8203b'
down_revision: Union[str, None] = '6408ab66eb8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('financial_transaction',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('amount', sa.Integer(), nullable=False),
                    sa.Column('transaction_code', sa.String(255), nullable=False),
                    sa.Column('status',
                              sa.Enum('PENDING', 'FAIL', 'DONE', name='financial_status_enum'),
                              nullable=False),
                    sa.Column('type_transaction',
                              sa.Enum('DEPOSIT', 'WITHDRAW', name='type_transaction_enum'),
                              nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('financial_transaction')
