"""add enum financial transaction in notification table

Revision ID: 7135e935b9f3
Revises: e66827776ec9
Create Date: 2023-11-25 23:05:57.216046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7135e935b9f3'
down_revision: Union[str, None] = 'e66827776ec9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE notification_type_enum ADD VALUE 'FINANCIAL_TRANSACTION'")


def downgrade() -> None:
    op.execute("ALTER TYPE notification_type_enum DROP VALUE 'FINANCIAL_TRANSACTION'")
