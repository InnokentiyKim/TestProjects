import os


POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

TOKEN_TTL_SEC = int(os.getenv("TOKEN_TTL_SEC", 24 * 60 * 60))

ADMIN_NAME = os.getenv("ADMIN_NAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")