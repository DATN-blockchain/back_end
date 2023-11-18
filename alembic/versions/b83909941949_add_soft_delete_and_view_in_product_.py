"""add soft delete and view in product table

Revision ID: b83909941949
Revises: 5e354ee8f0a6
Create Date: 2023-11-18 14:03:52.164352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b83909941949'
down_revision: Union[str, None] = '5e354ee8f0a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('product', sa.Column('soft_delete', sa.Boolean(),
                                       nullable=True, server_default=sa.text('false')))
    op.add_column('product', sa.Column('view', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    op.drop_column('product', 'soft_delete')
    op.drop_column('product', 'view')
