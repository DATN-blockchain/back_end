"""create table classify goods

Revision ID: 13644f6ef3a3
Revises: d4ff1dad4f72
Create Date: 2023-11-18 21:11:56.524546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '13644f6ef3a3'
down_revision: Union[str, None] = 'd4ff1dad4f72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('classify_goods',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('data', sa.JSON(), nullable=False),
                    sa.Column('product_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('classify_goods')
