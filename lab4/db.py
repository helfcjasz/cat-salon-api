import os

import psycopg

DSN = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres",
)


def get_connection() -> psycopg.Connection:
    """Повертає нове з'єднання з БД."""
    return psycopg.connect(DSN)
