"""Remove user role and status

Revision ID: 509115474d51
Revises: 4d4c8a2e1646
Create Date: 2015-02-15 15:20:57.983000

"""

# revision identifiers, used by Alembic.
revision = '509115474d51'
down_revision = '4d4c8a2e1646'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('auth_user', 'status')
    op.drop_column('auth_user', 'role')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('auth_user', sa.Column('role', sa.SMALLINT(), nullable=False))
    op.add_column('auth_user', sa.Column('status', sa.SMALLINT(), nullable=False))
    ### end Alembic commands ###