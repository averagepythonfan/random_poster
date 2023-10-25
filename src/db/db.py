from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import URL
from sqlalchemy.engine import create_engine


from src.config import (
    POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT, POSTGRES_DB
)


db_url_async = URL.create(
    drivername="postgresql+asyncpg",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=POSTGRES_DB
)


db_url_sync = URL.create(
    drivername="postgresql+psycopg2",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=POSTGRES_DB
)


engine_sync = create_engine(url=db_url_sync)
engine = create_async_engine(url=db_url_async)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)