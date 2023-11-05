import os

TOKEN: str = os.getenv("TOKEN")
CHAT_ID = -(int(os.getenv("CHAT_ID")))
ADMIN = int(os.getenv("ADMIN"))
ADMIN2 = int(os.getenv("ADMIN2"))

admins = [ADMIN, ADMIN2]

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

REDIS_HOST: str = os.getenv("REDIS", "redis")
REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")

TG_CHANNEL_LINK: str = os.getenv("TG_CHANNEL_LINK")