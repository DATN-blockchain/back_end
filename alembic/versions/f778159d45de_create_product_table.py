"""create product table

Revision ID: f778159d45de
Revises: 533cdac99d6e
Create Date: 2023-09-22 09:30:04.442038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f778159d45de'
down_revision: Union[str, None] = '533cdac99d6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('product',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('banner', sa.String(length=255), nullable=True),
                    sa.Column('description', sa.String(length=255), nullable=True),
                    sa.Column('price', sa.Integer, nullable=True),
                    sa.Column('quantity', sa.Integer, nullable=True),
                    sa.Column('hashed_data', sa.String(length=255), nullable=True),
                    sa.Column('product_status', sa.Enum('PUBLISH', 'PRIVATE', 'CLOSE', name='status_product_enum'),
                              nullable=False),
                    sa.Column('product_type',
                              sa.Enum('SEEDLING_COMPANY', 'FARMER', 'MANUFACTURER', name='type_product_enum'),
                              nullable=False),
                    sa.Column('created_by', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('product')
