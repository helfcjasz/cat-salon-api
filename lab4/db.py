import os

import psycopg

DSN = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres",
)


def get_connection() -> psycopg.Connection:
    return psycopg.connect(DSN)
