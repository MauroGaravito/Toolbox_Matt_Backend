"""Updated models to match AI workflow

Revision ID: cdde7ca3f111
Revises: 9da0b5d9da54
Create Date: 2025-03-20 14:04:05.199296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import datetime

# revision identifiers, used by Alembic.
revision: str = 'cdde7ca3f111'
down_revision: Union[str, None] = '9da0b5d9da54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 🔴 Eliminar primero las tablas dependientes antes de `toolbox_talks`
    op.drop_table('attendees')
    op.drop_table('risks_and_controls')
    op.drop_table('documents')
    op.drop_table('toolbox_talks')

    # 🟢 Crear nuevas tablas
    op.create_table(
        'generated_toolbox_talks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('topic', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(), default=datetime.datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generated_toolbox_talks_id'), 'generated_toolbox_talks', ['id'], unique=False)

    op.create_table(
        'reference_documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uploaded_by', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), default=datetime.datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reference_documents_id'), 'reference_documents', ['id'], unique=False)

    op.create_table(
        'signatures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('toolbox_talk_id', sa.Integer(), sa.ForeignKey('generated_toolbox_talks.id')),
        sa.Column('signer_name', sa.String(), nullable=False),
        sa.Column('signer_email', sa.String(), nullable=True),
        sa.Column('signature_image', sa.Text(), nullable=True),
        sa.Column('signed_at', sa.DateTime(), default=datetime.datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_signatures_id'), 'signatures', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # 🔴 Primero eliminamos las nuevas tablas antes de restaurar las antiguas
    op.drop_index(op.f('ix_signatures_id'), table_name='signatures')
    op.drop_table('signatures')
    op.drop_index(op.f('ix_reference_documents_id'), table_name='reference_documents')
    op.drop_table('reference_documents')
    op.drop_index(op.f('ix_generated_toolbox_talks_id'), table_name='generated_toolbox_talks')
    op.drop_table('generated_toolbox_talks')

    # 🟢 Restauramos las tablas antiguas
    op.create_table(
        'toolbox_talks',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(), nullable=False),
        sa.Column('description', sa.TEXT(), nullable=True),
        sa.Column('created_by', sa.INTEGER(), sa.ForeignKey('users.id')),
        sa.Column('document_url', sa.VARCHAR(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_toolbox_talks_id', 'toolbox_talks', ['id'], unique=False)

    op.create_table(
        'documents',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('toolbox_talk_id', sa.INTEGER(), sa.ForeignKey('toolbox_talks.id')),
        sa.Column('file_name', sa.VARCHAR(), nullable=False),
        sa.Column('file_path', sa.VARCHAR(), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(), default=datetime.datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_documents_id', 'documents', ['id'], unique=False)

    op.create_table(
        'risks_and_controls',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('toolbox_talk_id', sa.INTEGER(), sa.ForeignKey('toolbox_talks.id')),
        sa.Column('risk_description', sa.TEXT(), nullable=False),
        sa.Column('control_measures', sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_risks_and_controls_id', 'risks_and_controls', ['id'], unique=False)

    op.create_table(
        'attendees',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('toolbox_talk_id', sa.INTEGER(), sa.ForeignKey('toolbox_talks.id')),
        sa.Column('worker_name', sa.VARCHAR(), nullable=False),
        sa.Column('worker_email', sa.VARCHAR(), nullable=True),
        sa.Column('signature', sa.TEXT(), nullable=True),
        sa.Column('attended_at', sa.DateTime(), default=datetime.datetime.utcnow),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_attendees_id', 'attendees', ['id'], unique=False)
