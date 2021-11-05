import asyncio

from .database import connect
from .models import Base


async def create_auth_tables():
    engine, _ = connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_auth_tables():
    engine, _ = connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def create_auth_tables_cli():
    asyncio.run(create_auth_tables())
