"""create grow up table

Revision ID: cfa938f5d2ce
Revises: 795beb4cef95
Create Date: 2023-10-01 21:38:08.741407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'cfa938f5d2ce'
down_revision: Union[str, None] = '795beb4cef95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('grow_up',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('image', sa.String(length=255), nullable=True),
                    sa.Column('video', sa.String(length=255), nullable=True),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('hashed_data', sa.String(length=255), nullable=True),
                    sa.Column('product_farmer_id', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['product_farmer_id'], ['product_farmer.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('grow_up')
