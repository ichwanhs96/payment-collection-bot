"""init customer information table

Revision ID: ead20383e104
Revises: 
Create Date: 2024-12-08 18:21:06.037412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ead20383e104'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
           'customer_banking_information',
           sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, unique=True),
           sa.Column('account_number', sa.String(length=50)),
           sa.Column('customer_name', sa.String(length=50)),
           sa.Column('total_due_amount', sa.Integer),
           sa.Column('principal_amount', sa.Integer),
           sa.Column('interest', sa.Integer),
           sa.Column('penalty', sa.Integer),
           sa.Column('product_name', sa.String(length=100)),
           sa.Column('due_date', sa.Date),
           sa.Column('identity_number', sa.String(length=50)),
           sa.Column('address', sa.String(length=100))
        )


def downgrade() -> None:
    op.drop_table('customer_banking_information')
