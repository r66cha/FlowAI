"""Database configuration schema"""

# -- Imports

from pydantic import BaseModel, PostgresDsn
from src.core.repository.database.db_config import db_url


# -- Exports

__all__ = ["DatabaseConfigSchema"]

# --


class DatabaseConfigSchema(BaseModel):
    """Configuration schema for the database connection and SQLAlchemy engine."""

    url_api: PostgresDsn = db_url.get_DB_URL_API
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
