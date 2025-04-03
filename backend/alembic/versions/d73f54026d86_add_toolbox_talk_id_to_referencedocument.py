"""Add toolbox_talk_id to ReferenceDocument

Revision ID: d73f54026d86
Revises: fc521ddecd43
Create Date: 2025-03-25 19:31:27.756959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd73f54026d86'
down_revision: Union[str, None] = 'fc521ddecd43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ya no intentamos crear la columna, porque ya existe
    # Solo agregamos la foreign key si no la tenías
    op.create_foreign_key(
        'fk_reference_documents_toolbox_talk_id_generated_toolbox_talks',
        'reference_documents',
        'generated_toolbox_talks',
        ['toolbox_talk_id'],
        ['id']
    )




def downgrade() -> None:
    op.drop_constraint(
        'fk_reference_documents_toolbox_talk_id_generated_toolbox_talks',
        'reference_documents',
        type_='foreignkey'
    )


