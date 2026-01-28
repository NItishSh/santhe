#!/bin/bash
SERVICE_NAME=$1

if [ -z "$SERVICE_NAME" ]; then
    echo "Usage: $0 <service-name>"
    exit 1
fi

SERVICE_DIR="services/$SERVICE_NAME"
if [ ! -d "$SERVICE_DIR" ]; then
    echo "Service $SERVICE_NAME not found"
    exit 1
fi

echo "Bootstrapping Alembic for $SERVICE_NAME..."

# 1. Create Directories
mkdir -p "$SERVICE_DIR/migrations/versions"

# 2. Create alembic.ini
cat > "$SERVICE_DIR/alembic.ini" <<EOF
[alembic]
script_location = migrations
prepend_sys_path = .
[post_write_hooks]
[loggers]
keys = root,sqlalchemy,alembic
[handlers]
keys = console
[formatters]
keys = generic
[logger_root]
level = WARN
handlers = console
qualname =
[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine
[logger_alembic]
level = INFO
handlers =
qualname = alembic
[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic
[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
EOF

# 3. Create migrations/env.py
cat > "$SERVICE_DIR/migrations/env.py" <<EOF
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

sys.path.append(os.getcwd())

from config.settings import settings
from src.database import Base
# Import models to ensure they are registered with Base.metadata
from src import models

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
EOF

# 4. Create script.py.mako
cat > "$SERVICE_DIR/migrations/script.py.mako" <<EOF
"""\${message}

Revision ID: \${up_revision}
Revises: \${down_revision | comma,n}
Create Date: \${create_date}

"""
from alembic import op
import sqlalchemy as sa
\${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = \${repr(up_revision)}
down_revision = \${repr(down_revision)}
branch_labels = \${repr(branch_labels)}
depends_on = \${repr(depends_on)}


def upgrade() -> None:
    \${upgrades if upgrades else "pass"}


def downgrade() -> None:
    \${downgrades if downgrades else "pass"}
EOF

# 5. Update requirements.txt
if ! grep -q "alembic" "$SERVICE_DIR/requirements.txt"; then
    echo "alembic>=1.13.0" >> "$SERVICE_DIR/requirements.txt"
fi
if ! grep -q "psycopg" "$SERVICE_DIR/requirements.txt"; then
    echo "psycopg[binary]>=3.2.0" >> "$SERVICE_DIR/requirements.txt"
fi

# 6. Comment out create_all in main.py
# Using sed to comment out the line containing Base.metadata.create_all
if [ -f "$SERVICE_DIR/src/main.py" ]; then
    sed -i.bak 's/Base.metadata.create_all/# Base.metadata.create_all/g' "$SERVICE_DIR/src/main.py"
    rm "$SERVICE_DIR/src/main.py.bak"
    echo "Disabled create_all in main.py"
fi

echo "Done for $SERVICE_NAME"
