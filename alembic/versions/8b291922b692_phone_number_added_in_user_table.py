"""phone_number added in user table

Revision ID: 8b291922b692
Revises: 0ce2a4f84482
Create Date: 2023-10-09 12:15:18.429404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b291922b692'
down_revision: Union[str, None] = '0ce2a4f84482'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_column('users', 'phone_number')

