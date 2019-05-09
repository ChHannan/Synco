"""files table

Revision ID: 07726143a2b3
Revises: e3db085e3e5e
Create Date: 2018-11-18 23:11:45.423096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07726143a2b3'
down_revision = 'e3db085e3e5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_timestamp'), 'file', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_file_timestamp'), table_name='file')
    op.drop_table('file')
    # ### end Alembic commands ###