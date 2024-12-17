"""create customer banking dummy data

Revision ID: 16a9f0aafeb8
Revises: ead20383e104
Create Date: 2024-12-08 18:33:32.808014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision: str = '16a9f0aafeb8'
down_revision: Union[str, None] = 'ead20383e104'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # retrieve customer_banking_information_table
    Base = declarative_base()
    customer_banking_information_table = sa.Table('customer_banking_information',
        Base.metadata,
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
        sa.Column('address', sa.String(length=100)),
        schema=None
    )
    # Inserting dummy data
    op.bulk_insert(
        customer_banking_information_table,
        [
            {
                'id': 1,
                'account_number': 'DDB2409001',
                'customer_name': 'Muhammad Faiz Bin Hassan',
                'total_due_amount': 2500,
                'principal_amount': 1750,
                'interest': 500,
                'penalty': 250,
                'product_name': 'Dean Corp Personal Loan',
                'due_date': '2024-12-31',
                'identity_number': '12409120324',
                'address': '12, Jalan Putra Perdana, Taman Tasik Damai, Kuala Lumpur'
            },
            {
                'id': 2,
                'account_number': 'DDB2409040',
                'customer_name': 'Trần Quang Dũng',
                'total_due_amount': 45340,
                'principal_amount': 31738,
                'interest': 9068,
                'penalty': 4534,
                'product_name': 'Dean Special Loan',
                'due_date': '2024-12-31',
                'identity_number': '12409120363',
                'address': '345/89 Đường Vĩnh Viễn, Phường 4, Quận 10, TP.HCM'
            }
        ]
    )


def downgrade() -> None:
    pass
