"""empty message

Revision ID: 87a38e209370
Revises: b3fcc3cce3c2
Create Date: 2019-06-05 21:16:21.364947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87a38e209370'
down_revision = 'b3fcc3cce3c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('best_streak', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('current_streak', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'current_streak')
    op.drop_column('user', 'best_streak')
    # ### end Alembic commands ###