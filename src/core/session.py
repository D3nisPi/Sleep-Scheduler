from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings

engine = create_async_engine(
    settings.db.url,
    future=True,
    echo=settings.engine.echo,
    pool_size=settings.engine.pool_size,
    max_overflow=settings.engine.max_overflow
)

async_session_factory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False
)


async def get_session():
    async with async_session_factory() as session:
        yield session
