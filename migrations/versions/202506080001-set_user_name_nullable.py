"""set user name nullable

Revision ID: d6f7ae8a92bd
Revises: 2d35ed3aefc6
Create Date: 2025-06-08 00:01:24.282426

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d6f7ae8a92bd"
down_revision: Union[str, None] = "2d35ed3aefc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users", "user_name", existing_type=sa.VARCHAR(length=32), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "user_name",
        existing_type=sa.VARCHAR(length=32),
        nullable=False,
    )
    # ### end Alembic commands ###
