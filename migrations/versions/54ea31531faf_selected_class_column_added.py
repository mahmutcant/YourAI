"""selected class column added

Revision ID: 54ea31531faf
Revises: 3231eccb322c
Create Date: 2023-09-05 19:41:17.734557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54ea31531faf'
down_revision = '3231eccb322c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('savedmodels', schema=None) as batch_op:
        batch_op.add_column(sa.Column('selectedLabel', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('savedmodels', schema=None) as batch_op:
        batch_op.drop_column('selectedLabel')

    # ### end Alembic commands ###
