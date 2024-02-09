"""empty message

Revision ID: 02f3dccb4c16
Revises: 3f9eb5c50189
Create Date: 2024-02-09 06:44:12.628319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02f3dccb4c16'
down_revision = '3f9eb5c50189'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('viewers', schema=None) as batch_op:
        batch_op.drop_constraint('viewers_best_gamer_id_fkey', type_='foreignkey')
        batch_op.drop_column('best_gamer_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('viewers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('best_gamer_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('viewers_best_gamer_id_fkey', 'gamers', ['best_gamer_id'], ['id'])

    # ### end Alembic commands ###
