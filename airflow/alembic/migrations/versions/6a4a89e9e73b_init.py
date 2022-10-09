"""init

Revision ID: 6a4a89e9e73b
Revises: 
Create Date: 2022-10-09 18:26:01.336815

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = '6a4a89e9e73b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('currenciesrate',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('currency', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('rate', sa.Float(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('currenciesrate')
