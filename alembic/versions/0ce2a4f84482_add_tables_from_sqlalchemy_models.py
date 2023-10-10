"""add tables from sqlalchemy models

Revision ID: 0ce2a4f84482
Revises: 12b13e613504
Create Date: 2023-10-09 12:11:18.323937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0ce2a4f84482'
down_revision: Union[str, None] = '12b13e613504'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('investments', 'amount',
               existing_type=sa.REAL(),
               type_=sa.Float(),
               existing_nullable=False)
    op.alter_column('investments', 'opening_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.create_index(op.f('ix_public_investments_id'), 'investments', ['id'], unique=False, schema='public')
    op.drop_constraint('investments_fk', 'investments', type_='foreignkey')
    op.create_foreign_key(None, 'investments', 'users', ['user_id'], ['id'], source_schema='public', referent_schema='public', ondelete='CASCADE')
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.create_index(op.f('ix_public_users_id'), 'users', ['id'], unique=False, schema='public')
    op.drop_constraint('votes_investment_id_fkey', 'votes', type_='foreignkey')
    op.drop_constraint('votes_user_id_fkey', 'votes', type_='foreignkey')
    op.create_foreign_key(None, 'votes', 'users', ['user_id'], ['id'], referent_schema='public', ondelete='CASCADE')
    op.create_foreign_key(None, 'votes', 'investments', ['investment_id'], ['id'], referent_schema='public', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'votes', type_='foreignkey')
    op.drop_constraint(None, 'votes', type_='foreignkey')
    op.create_foreign_key('votes_user_id_fkey', 'votes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('votes_investment_id_fkey', 'votes', 'investments', ['investment_id'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_public_users_id'), table_name='users', schema='public')
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.drop_constraint(None, 'investments', schema='public', type_='foreignkey')
    op.create_foreign_key('investments_fk', 'investments', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_public_investments_id'), table_name='investments', schema='public')
    op.alter_column('investments', 'opening_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default=sa.text('now()'))
    op.alter_column('investments', 'amount',
               existing_type=sa.Float(),
               type_=sa.REAL(),
               existing_nullable=False)
    # ### end Alembic commands ###
