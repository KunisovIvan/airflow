from sqlmodel import SQLModel, Field

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import PG

engine = create_async_engine(PG.URL, echo=True, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


class CurrenciesRate(SQLModel, table=True):
    id: int = Field(primary_key=True)
    currency: str
    rate: float
