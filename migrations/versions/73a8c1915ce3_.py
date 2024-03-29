"""empty message

Revision ID: 73a8c1915ce3
Revises: 1edabb6d39a4
Create Date: 2020-11-27 10:48:56.723476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73a8c1915ce3'
down_revision = '1edabb6d39a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedules', sa.Column('date_of_overnight_stay', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedules', 'date_of_overnight_stay')
    # ### end Alembic commands ###
