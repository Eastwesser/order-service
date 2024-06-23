"""after tests update

Revision ID: 7ce2091a24c8
Revises: 15db83a354c8
Create Date: 2024-06-23 19:08:04.634171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ce2091a24c8'
down_revision: Union[str, None] = '15db83a354c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
