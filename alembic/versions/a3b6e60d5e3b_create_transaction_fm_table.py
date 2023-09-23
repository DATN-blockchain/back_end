"""create transaction FM table

Revision ID: a3b6e60d5e3b
Revises: 42a2dded7c79
Create Date: 2023-09-22 16:07:58.077391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3b6e60d5e3b'
down_revision: Union[str, None] = '42a2dded7c79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('transaction_fm',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('hashed_data', sa.String(length=255), nullable=True),
                    sa.Column('status', sa.String(length=255), nullable=True),
                    sa.Column('price', sa.Integer, nullable=True),
                    sa.Column('quantity', sa.Integer, nullable=True),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('product_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('transaction_FM')
