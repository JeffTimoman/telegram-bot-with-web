"""empty message

Revision ID: 7d7289548a33
Revises: 9fcfd9bb3764
Create Date: 2023-12-01 23:26:43.696196

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7d7289548a33'
down_revision = '9fcfd9bb3764'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('command', schema=None) as batch_op:
        batch_op.alter_column('expired_date',
               existing_type=mysql.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('command', schema=None) as batch_op:
        batch_op.alter_column('expired_date',
               existing_type=mysql.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###
