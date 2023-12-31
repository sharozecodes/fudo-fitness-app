"""removes date_of_birth, height and weight from user model

Revision ID: 3c793110b382
Revises: d164a8f206db
Create Date: 2023-10-06 20:32:38.062943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c793110b382'
down_revision = 'd164a8f206db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('weight')
        batch_op.drop_column('height')
        batch_op.drop_column('date_of_birth')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_of_birth', sa.DATE(), nullable=False))
        batch_op.add_column(sa.Column('height', sa.FLOAT(), nullable=False))
        batch_op.add_column(sa.Column('weight', sa.FLOAT(), nullable=False))

    # ### end Alembic commands ###
