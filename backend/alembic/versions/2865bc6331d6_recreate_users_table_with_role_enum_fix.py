"""Recreate users table with role enum fix

Revision ID: 2865bc6331d6
Revises: cdde7ca3f111
Create Date: 2025-03-22 13:44:50.432233
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = '2865bc6331d6'
down_revision: Union[str, None] = 'cdde7ca3f111'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # ✅ Crear Enum solo si no existe
    if not conn.dialect.has_type(conn, "roleenum"):
        role_enum = postgresql.ENUM('admin', 'supervisor', 'worker', name='roleenum')
        role_enum.create(conn, checkfirst=True)

    # ✅ Crear tabla users solo si no existe
    if 'users' not in inspector.get_table_names():
        op.create_table(
            'users',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('username', sa.String),
            sa.Column('email', sa.String),
            sa.Column('hashed_password', sa.String),
            sa.Column('role', sa.Enum('admin', 'supervisor', 'worker', name='roleenum')),
            sa.Column('created_at', sa.DateTime),
        )
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
        op.create_index(op.f('ix_users_id'), 'users', ['id'])
        op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
        op.create_foreign_key(None, 'activity_logs', 'users', ['user_id'], ['id'])
        op.create_foreign_key(None, 'generated_toolbox_talks', 'users', ['created_by'], ['id'])
        op.create_foreign_key(None, 'reference_documents', 'users', ['uploaded_by'], ['id'])


def downgrade() -> None:
    op.drop_constraint(None, 'reference_documents', type_='foreignkey')
    op.drop_constraint(None, 'generated_toolbox_talks', type_='foreignkey')
    op.drop_constraint(None, 'activity_logs', type_='foreignkey')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.execute('DROP TYPE IF EXISTS roleenum')
