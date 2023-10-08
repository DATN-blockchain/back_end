"""create activity table

Revision ID: 765ca31342b5
Revises: 62b239162381
Create Date: 2023-10-08 12:35:13.420346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '765ca31342b5'
down_revision: Union[str, None] = '62b239162381'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('activity',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('data', sa.JSON(), nullable=False),
                    sa.Column('product_id', sa.String(length=255), nullable=False),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('activity')