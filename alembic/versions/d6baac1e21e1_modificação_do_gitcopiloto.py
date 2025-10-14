"""modificação do gitcopiloto

Revision ID: d6baac1e21e1
Revises: f6b7ffcc01d1
Create Date: 2025-10-14 17:20:18.784520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6baac1e21e1'
down_revision: Union[str, Sequence[str], None] = 'f6b7ffcc01d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
