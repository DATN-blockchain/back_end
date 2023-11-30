"""create messenger table

Revision ID: 8531e54f09ef
Revises: 67f1cd766b32
Create Date: 2023-11-29 23:29:05.362010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '8531e54f09ef'
down_revision: Union[str, None] = '67f1cd766b32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('messenger',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('sender_id', sa.String(length=255), nullable=False),
                    sa.Column('receiver_id', sa.String(length=255), nullable=True),
                    sa.Column('content', sa.String(length=500), nullable=True),
                    sa.Column('data', sa.JSON(), nullable=True),
                    sa.Column('is_read', sa.Boolean(), nullable=True, server_default=sa.text('false')),
                    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], ondelete="CASCADE"),
                    sa.Column('create_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('messenger')
