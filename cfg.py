import os

DATABASE_CONFIG = {
    "dbname": os.environ.get("DB_NAME", ""),
    "user": os.environ.get("DB_USER", ""),
    "password": os.environ.get("DB_PASS", ""),
    "host": os.environ.get("DB_HOST", ""),
    "port": os.environ.get("DB_PORT", "")
}

GIT_DIR = os.environ.get("GIT_DIR", "")
