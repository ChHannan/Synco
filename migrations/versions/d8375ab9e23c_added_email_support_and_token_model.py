"""Added email support and token model

Revision ID: d8375ab9e23c
Revises: aba1335a28ed
Create Date: 2018-11-26 00:25:37.227939

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8375ab9e23c'
down_revision = 'aba1335a28ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=128), nullable=True),
    sa.Column('type', sa.String(length=10), nullable=True),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_token'), 'token', ['token'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_token_token'), table_name='token')
    op.drop_table('token')
    # ### end Alembic commands ###
