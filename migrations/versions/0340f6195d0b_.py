"""empty message

Revision ID: 0340f6195d0b
Revises: 
Create Date: 2021-06-02 13:01:53.159562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0340f6195d0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('genre', sa.String(), nullable=True),
    sa.Column('director', sa.String(), nullable=True),
    sa.Column('actors', sa.String(), nullable=True),
    sa.Column('cover', sa.String(), nullable=True),
    sa.Column('plot', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movies')
    # ### end Alembic commands ###
