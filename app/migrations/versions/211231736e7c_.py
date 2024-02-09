"""empty message

Revision ID: 211231736e7c
Revises: 579623acb974
Create Date: 2024-02-09 06:04:59.841806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '211231736e7c'
down_revision = '579623acb974'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gamers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('viewer_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'viewers', ['viewer_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gamers', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('viewer_id')

    # ### end Alembic commands ###
