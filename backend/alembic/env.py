import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

# ✅ Cargar .env correctamente
from dotenv import load_dotenv
load_dotenv()

# ✅ Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# ✅ Importar modelos y base de datos
from models import Base

# Alembic config object
config = context.config

# Configurar logging si hay archivo
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadatos de los modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using env variable."""
    url = os.getenv("DATABASE_URL")

    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Decide si ejecutar en modo online u offline
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
