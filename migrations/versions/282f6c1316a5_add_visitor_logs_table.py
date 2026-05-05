"""add visitor_logs table

Revision ID: 282f6c1316a5
Revises: 0f1ff944e5d9
Create Date: 2026-04-16 12:26:08.894425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '282f6c1316a5'
down_revision: Union[str, Sequence[str], None] = '0f1ff944e5d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create visitor_logs table for request analytics."""
    op.create_table('visitor_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.String(length=45), nullable=False),
    sa.Column('path', sa.String(length=512), nullable=False),
    sa.Column('method', sa.String(length=10), nullable=False),
    sa.Column('status_code', sa.Integer(), nullable=True),
    sa.Column('user_agent', sa.String(length=512), nullable=True),
    sa.Column('referrer', sa.String(length=512), nullable=True),
    sa.Column('response_time_ms', sa.Integer(), nullable=True),
    sa.Column('country', sa.String(length=64), nullable=True),
    sa.Column('city', sa.String(length=128), nullable=True),
    sa.Column('is_unique', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_visitor_ip_created', 'visitor_logs', ['ip_address', 'created_at'], unique=False)
    op.create_index(op.f('ix_visitor_logs_created_at'), 'visitor_logs', ['created_at'], unique=False)


def downgrade() -> None:
    """Drop visitor_logs table."""
    op.drop_index(op.f('ix_visitor_logs_created_at'), table_name='visitor_logs')
    op.drop_index('idx_visitor_ip_created', table_name='visitor_logs')
    op.drop_table('visitor_logs')
