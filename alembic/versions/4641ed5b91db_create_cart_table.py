"""create cart table

Revision ID: 4641ed5b91db
Revises: 0e4dfb86fe4a
Create Date: 2023-11-11 11:34:21.377765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4641ed5b91db'
down_revision: Union[str, None] = '0e4dfb86fe4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('cart',
                    sa.Column('id', sa.String(length=255), nullable=False),
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
    op.drop_table('cart')
