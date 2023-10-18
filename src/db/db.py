from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import URL


from src.config import (
    POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT, POSTGRES_DB
)


db_url = URL.create(
    drivername="postgresql+asyncpg",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=POSTGRES_DB
)


engine = create_async_engine(url=db_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)