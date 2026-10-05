import psycopg
from pgvector.psycopg import register_vector

from app.config import settings


def conectar() -> psycopg.Connection:
    conn = psycopg.connect(settings.database_url, connect_timeout=5)
    register_vector(conn)
    return conn
