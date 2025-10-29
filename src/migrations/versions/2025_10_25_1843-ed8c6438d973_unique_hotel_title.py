"""unique hotel title

Revision ID: ed8c6438d973
Revises: fda376c885e5
Create Date: 2025-10-25 18:43:50.270084

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ed8c6438d973"
down_revision: Union[str, Sequence[str], None] = "fda376c885e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "hotels", ["title"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "hotels", type_="unique")
