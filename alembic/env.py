import logging
import os
from logging.config import fileConfig

from dotenv import load_dotenv

# Load environment variables (local overrides default)
load_dotenv(".env", override=False)
load_dotenv(".env.local", override=True)

from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context
from models import *  # ensure all models are imported

# Alembic Config object (from alembic.ini)
config = context.config

# Set up logging from config file
if config.config_file_name:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")

# SQLModel metadata for migrations
target_metadata = SQLModel.metadata

# Get database URL from environment
DATABASE_URL = os.getenv("ALEMBIC_DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("ALEMBIC_DATABASE_URL environment variable is not set")

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if TEST_DATABASE_URL:
    DATABASE_URL = TEST_DATABASE_URL

# Inject DB URL into Alembic config
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    """Run Alembic migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    logger.info("Running offline migrations")
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run Alembic migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        logger.info("Running online migrations")
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
