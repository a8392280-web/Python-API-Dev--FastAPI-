"""add fk to post table

Revision ID: d8f19fd10d24
Revises: ad28a1782bc0
Create Date: 2025-12-29 14:52:44.644457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8f19fd10d24'
down_revision: Union[str, Sequence[str], None] = 'ad28a1782bc0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'owner_id')
    pass
