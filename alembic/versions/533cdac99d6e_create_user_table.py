"""create user table

Revision ID: 533cdac99d6e
Revises: 
Create Date: 2023-09-21 22:41:43.271248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '533cdac99d6e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.String(length=255), nullable=False),
                    sa.Column('username', sa.String(length=255), nullable=False),
                    sa.Column('full_name', sa.String(length=255), nullable=True),
                    sa.Column('avatar', sa.String(length=255), nullable=True),
                    sa.Column('phone', sa.String(length=255), nullable=True),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.Column('is_active', sa.Boolean(), server_default=sa.text('false'), nullable=False),
                    sa.Column('private_key', sa.String(length=255), nullable=True),
                    sa.Column('address_wallet', sa.String(length=255), nullable=True),
                    sa.Column('address_real', sa.String(length=255), nullable=True),
                    sa.Column('hashed_data', sa.String(length=255), nullable=True),
                    sa.Column('birthday', sa.Date(), nullable=True),
                    sa.Column('hashed_password', sa.String(), nullable=True),
                    sa.Column('verify_code', sa.String(), nullable=True),
                    sa.Column('system_role',
                              sa.Enum('SUPPER_ADMIN', 'ADMIN', 'FARMER', 'SEEDLING_COMPANY', 'MANUFACTURER', 'MEMBER',
                                      name='system_role_enum'),
                              nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('user')
