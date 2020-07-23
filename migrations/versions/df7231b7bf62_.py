"""empty message

Revision ID: df7231b7bf62
Revises: 48b937a669cb
Create Date: 2020-06-25 16:38:22.707523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df7231b7bf62'
down_revision = '48b937a669cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('created_on', sa.DATETIME(), nullable=True),
    sa.Column('updated_on', sa.DATETIME(), nullable=True),
    sa.Column('created_by', sa.INTEGER(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('fullname', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('sign_in_count', sa.Integer(), nullable=True),
    sa.Column('project_limits', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=20), nullable=True),
    sa.Column('last_activity_on', sa.DATETIME(), nullable=True),
    sa.Column('admin', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###