from asyncpg import Pool, create_pool
from app.config.settings import settings


class Database:
    _pool: Pool = None

    @classmethod
    async def connect(cls):
        if cls._pool is None:
            cls._pool = await create_pool(
                settings.database_url, min_size=2, max_size=10
            )

    @classmethod
    async def disconnect(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None

    @classmethod
    async def execute(cls, query: str, *args):
        async with cls._pool.acquire() as connection:
            return await connection.execute(query, *args)

    @classmethod
    async def fetch(cls, query: str, *args):
        async with cls._pool.acquire() as connection:
            return await connection.fetch(query, *args)

    @classmethod
    async def fetchrow(cls, query: str, *args):
        async with cls._pool.acquire() as connection:
            return await connection.fetchrow(query, *args)
