"""create detail description table

Revision ID: 767a955387c2
Revises: 4641ed5b91db
Create Date: 2023-11-11 13:45:13.850470

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '767a955387c2'
down_revision: Union[str, None] = '4641ed5b91db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('detail_description',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('title', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.String(length=500), nullable=True),
                    sa.Column('image', sa.String(length=255), nullable=True),
                    sa.Column('product_id', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('detail_description')
