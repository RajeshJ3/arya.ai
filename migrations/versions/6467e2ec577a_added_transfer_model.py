"""added Transfer model

Revision ID: 6467e2ec577a
Revises: 1028e72b0e51
Create Date: 2023-05-21 14:16:39.510144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6467e2ec577a'
down_revision = '1028e72b0e51'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transfers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('source_bank_account_id', sa.Integer(), nullable=True),
    sa.Column('destination_bank_account_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['destination_bank_account_id'], ['bank_accounts.id'], ),
    sa.ForeignKeyConstraint(['source_bank_account_id'], ['bank_accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transfers_id'), 'transfers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transfers_id'), table_name='transfers')
    op.drop_table('transfers')
    # ### end Alembic commands ###
