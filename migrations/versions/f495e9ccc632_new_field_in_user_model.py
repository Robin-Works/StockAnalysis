"""new field in user model

Revision ID: f495e9ccc632
Revises: a65df351ba70
Create Date: 2024-03-18 17:45:04.905860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f495e9ccc632'
down_revision = 'a65df351ba70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('aboutMe', sa.String(length=140), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('aboutMe')

    # ### end Alembic commands ###
