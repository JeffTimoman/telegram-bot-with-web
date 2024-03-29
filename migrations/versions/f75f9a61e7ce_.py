"""empty message

Revision ID: f75f9a61e7ce
Revises: 56c9d16cee2a
Create Date: 2023-12-02 13:13:41.346423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f75f9a61e7ce'
down_revision = '56c9d16cee2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('connected_user', schema=None) as batch_op:
        batch_op.alter_column('chat_id',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('connected_user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('chat_id',
               existing_type=sa.String(length=100),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)

    # ### end Alembic commands ###
