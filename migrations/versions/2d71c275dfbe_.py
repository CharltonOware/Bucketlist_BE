"""empty message

Revision ID: 2d71c275dfbe
Revises: 
Create Date: 2022-08-16 22:48:36.632313

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2d71c275dfbe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revoked_tokens')
    op.drop_constraint('bucketlists_created_by_fkey', 'bucketlists', type_='foreignkey')
    op.drop_column('bucketlists', 'created_by')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bucketlists', sa.Column('created_by', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('bucketlists_created_by_fkey', 'bucketlists', 'users', ['created_by'], ['id'])
    op.create_table('revoked_tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('jti', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='revoked_tokens_pkey')
    )
    # ### end Alembic commands ###