"""create reply_comment table

Revision ID: f590fc380416
Revises: d8bc080f46af
Create Date: 2023-10-07 16:25:33.507281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f590fc380416'
down_revision: Union[str, None] = 'd8bc080f46af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('reply_comment',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('content', sa.String(length=255), nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('comment_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('reply_comment')
