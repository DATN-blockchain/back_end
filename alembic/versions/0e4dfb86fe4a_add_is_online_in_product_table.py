"""add is online in product table

Revision ID: 0e4dfb86fe4a
Revises: 55ed041c0389
Create Date: 2023-11-10 14:13:56.246923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0e4dfb86fe4a'
down_revision: Union[str, None] = '55ed041c0389'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('product', sa.Column('is_sale', sa.Boolean(), nullable=True, server_default=sa.text('false')))


def downgrade() -> None:
    op.drop_column('product', 'is_sale')
