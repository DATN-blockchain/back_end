"""create leaderboard table

Revision ID: 55ed041c0389
Revises: 76b958e8203b
Create Date: 2023-11-01 15:12:46.919508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55ed041c0389'
down_revision: Union[str, None] = '76b958e8203b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('leaderboard',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('number_of_sales', sa.Integer(), nullable=True),
                    sa.Column('quantity_sales', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.String(length=255), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('leaderboard')
