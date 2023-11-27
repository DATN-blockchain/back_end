"""feat: add description in user table

Revision ID: 1f8cf532d39b
Revises: 7135e935b9f3
Create Date: 2023-11-27 09:54:25.979287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f8cf532d39b'
down_revision: Union[str, None] = '7135e935b9f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('description', sa.String(500), nullable=True))


def downgrade() -> None:
    op.drop_column('user', 'description')
