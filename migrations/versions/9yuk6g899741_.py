"""empty message

Revision ID: 9yuk6g899741
Revises: h6rg67898907
Create Date: 2019-05-02 14:34:34.189871

"""

# revision identifiers, used by Alembic.
revision = '9yuk6g899741'
down_revision = 'h6rg67898907'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_users_email_id'), 'users', type_='unique')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq_users_email_id'), 'users', ['email_id'])
    ### end Alembic commands ###