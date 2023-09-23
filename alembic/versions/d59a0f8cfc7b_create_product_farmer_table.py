"""create product_farmer table

Revision ID: d59a0f8cfc7b
Revises: a3b6e60d5e3b
Create Date: 2023-09-22 22:28:07.664222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd59a0f8cfc7b'
down_revision: Union[str, None] = 'a3b6e60d5e3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('product_farmer',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('product_id', sa.String(length=255), nullable=False),
                    sa.Column('transaction_sf_id', sa.String(length=255), nullable=False),
                    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['transaction_sf_id'], ['transaction_sf.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('product_farmer')
