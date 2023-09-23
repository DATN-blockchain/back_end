"""create product manufacturer table

Revision ID: f9e87bb279a7
Revises: d59a0f8cfc7b
Create Date: 2023-09-22 22:40:29.672176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9e87bb279a7'
down_revision: Union[str, None] = 'd59a0f8cfc7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('product_manufacturer',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('transaction_fm_id', sa.String(length=255), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['transaction_fm_id'], ['transaction_fm.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('product_manufacturer')
