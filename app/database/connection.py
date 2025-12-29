from asyncpg import Pool, create_pool
from app.config import settings


class Database:
    pool: Pool = None

    @classmethod
    async def connect(cls):
        cls.pool = await create_pool(settings.database_url, min_size=2, max_size=10)

    @classmethod
    async def disconnect(cls):
        if cls.pool:
            await cls.pool.close()

    @classmethod
    async def execute(cls, query: str, *args):
        async with cls.pool.acquire() as connection:
            return await connection.execute(query, *args)

    @classmethod
    async def fetch(cls, query: str, *args):
        async with cls.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    @classmethod
    async def fetchrow(cls, query: str, *args):
        async with cls.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)


db = Database()
