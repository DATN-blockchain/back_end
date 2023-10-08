"""create notification table

Revision ID: 62b239162381
Revises: f590fc380416
Create Date: 2023-10-07 21:21:10.831447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '62b239162381'
down_revision: Union[str, None] = 'f590fc380416'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('notification',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('data', sa.JSON(), nullable=False),
                    sa.Column('unread', sa.Boolean(), server_default=sa.text("True")),
                    sa.Column('notification_type',
                              sa.Enum('SYSTEM_NOTIFICATION', 'PRODUCT_NOTIFICATION', 'SEEDLING_COMPANY_NOTIFICATION',
                                      'FRAMER_NOTIFICATION', 'MANUFACTURER_NOTIFICATION', 'TRANSACTION_NOTIFICATION',
                                      'POST_NOTIFICATION', 'COMMENT_NOTIFICATION',
                                      name='notification_type_enum'), nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('notification')
