"""create transaction SF table

Revision ID: 42a2dded7c79
Revises: f778159d45de
Create Date: 2023-09-22 16:04:46.677528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42a2dded7c79'
down_revision: Union[str, None] = 'f778159d45de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('transaction_sf',
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
    op.drop_table('transaction_SF')
