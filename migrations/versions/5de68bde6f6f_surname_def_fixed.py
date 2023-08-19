"""surname def fixed

Revision ID: 5de68bde6f6f
Revises: 15234b0cc41d
Create Date: 2023-08-19 22:40:13.070910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5de68bde6f6f'
down_revision = '15234b0cc41d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('surname', sa.String(), nullable=True))
        batch_op.drop_column('surnaname')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('surnaname', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('surname')

    # ### end Alembic commands ###