import logging
from os import environ

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

_engine = None
_SessionLocal = None


def connect(connection_string=None, echo=False):
    global _engine, _SessionLocal

    if connection_string is None:
        connection_string = environ.get(
            'CONNECTION_STRING', 'sqlite+aiosqlite:///./test.db'
        )

    _engine = create_async_engine(connection_string, echo=echo)
    _SessionLocal = sessionmaker(
        bind=_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    return _engine, _SessionLocal


def get_session() -> AsyncSession:
    return _SessionLocal()


async def get_db():
    db: AsyncSession = _SessionLocal()
    try:
        yield db
    except Exception as error:
        logging.warn(str(error))
        await db.rollback()
        await db.close()
    finally:
        await db.close()
