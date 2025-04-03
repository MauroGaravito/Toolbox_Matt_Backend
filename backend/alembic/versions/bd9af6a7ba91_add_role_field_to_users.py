"""Add role field to users

Revision ID: bd9af6a7ba91
Revises: 203bb4c1adf0
Create Date: 2025-03-20 11:45:11.066636

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Definir el nuevo tipo ENUM
role_enum = sa.Enum('admin', 'user', name='roleenum')

# Revision identifiers, used by Alembic
revision: str = 'bd9af6a7ba91'
down_revision: Union[str, None] = '203bb4c1adf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Crear el tipo ENUM antes de agregarlo a la tabla
    role_enum.create(op.get_bind())

    # Agregar la columna role con el tipo ENUM
    op.add_column('users', sa.Column('role', role_enum, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar la columna antes de eliminar el tipo ENUM
    op.drop_column('users', 'role')

    # Eliminar el tipo ENUM
    role_enum.drop(op.get_bind())
