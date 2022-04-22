"""init

Revision ID: 1496a59fdcb9
Revises: 
Create Date: 2022-04-22 15:55:08.195912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1496a59fdcb9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False)
    )
    pass


def downgrade():
    op.drop_table('user')
    pass

