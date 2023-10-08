"""create comment table

Revision ID: d8bc080f46af
Revises: cfa938f5d2ce
Create Date: 2023-10-07 16:21:56.761386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8bc080f46af'
down_revision: Union[str, None] = 'cfa938f5d2ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('comment',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('content', sa.String(length=255), nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('marketplace_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['marketplace_id'], ['marketplace.id'], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )

def downgrade() -> None:
    op.drop_table('comment')
