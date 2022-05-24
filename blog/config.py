import os


class Config:
    DEBUG = os.environ.get("DEBUG") in ("True", "true", 1, "1")
    SECRET_KEY = os.environ.get("SECRET_KEY", "abc")
    ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

    DB_NAME = os.environ.get("DB_NAME", "blog")
    DB_USER = os.environ.get("DB_USER", "blog")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "blog")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = os.environ.get("DB_PORT", "3306")

    SALT_ROUNDS = os.environ.get("SALT_ROUNDS", 12)
    JWT_SECRET = os.environ.get("JWT_SECRET", "abc")
