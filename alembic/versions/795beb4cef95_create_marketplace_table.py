"""create marketplace table

Revision ID: 795beb4cef95
Revises: f9e87bb279a7
Create Date: 2023-09-22 22:44:38.652779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '795beb4cef95'
down_revision: Union[str, None] = 'f9e87bb279a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('marketplace',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('hashed_data', sa.String(length=255), nullable=True),
                    sa.Column('order_type',
                              sa.Enum('SEEDLING_COMPANY', 'FARMER', 'MANUFACTURER', name='type_order_enum'),
                              nullable=False),
                    sa.Column('order_id', sa.String(length=255), nullable=False),
                    sa.Column('order_by', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['order_id'], ['product.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['order_by'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('marketplace')
