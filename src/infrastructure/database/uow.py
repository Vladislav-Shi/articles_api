from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


class AsyncUnitOfWork:
    def __init__(self, db_ur: str):
        self.engine = create_async_engine(db_ur)
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def session(self):
        async with self.session_factory() as session:
            async with session.begin():
                try:
                    yield session
                    await session.commit()
                except Exception:
                    await session.rollback()
                    raise
