from collections.abc import AsyncGenerator
from datetime import datetime

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import settings

async_engine = create_async_engine(
    url=settings.base_url, echo=True, pool_size=5, max_overflow=10
)

session_maker = async_sessionmaker(
    async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession | None]:
    async with session_maker() as session:
        yield session


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.naming_convention)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:
        cols = []
        columns_to_show = 3
        for idx, col in enumerate(self.__table__.columns.keys()):
            if idx < columns_to_show:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
