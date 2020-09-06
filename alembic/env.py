import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, engine_from_config, pool
from tenacity import retry, stop_after_delay

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(db_url):
    engine = create_engine(db_url)
    return engine.connect()


def set_sqlalchemy_url():
    MODEL_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    sys.path.append(MODEL_PATH)
    from src.config import get_db_url

    wait_for_postgres_to_come_up(get_db_url())
    config.set_main_option('sqlalchemy.url', get_db_url())


set_sqlalchemy_url()


# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support


def get_metadata():
    MODEL_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    sys.path.append(MODEL_PATH)
    from src.orm import metadata

    return metadata


target_metadata = get_metadata()

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
