"""changes

Revision ID: 6d5e679817cf
Revises: 5d17b251e57e
Create Date: 2019-04-04 19:21:10.393691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d5e679817cf'
down_revision = '5d17b251e57e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('process_doc', sa.Column('iduh', sa.Integer(), autoincrement=True, nullable=False))
    op.drop_column('process_doc', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('process_doc', sa.Column('id', sa.VARCHAR(length=40), autoincrement=False, nullable=False))
    op.drop_column('process_doc', 'iduh')
    # ### end Alembic commands ###
