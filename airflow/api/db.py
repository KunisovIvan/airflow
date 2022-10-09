from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from airflow.models import dto
from airflow.models import db


router = APIRouter()


@router.get("/currency", response_model=List[dto.CurrenciesRate])
async def get_currencies(session: AsyncSession = Depends(db.get_session)) -> List[dto.CurrenciesRate]:
    result = await session.execute(select(db.CurrenciesRate))
    currencies = result.scalars().all()
    return [dto.CurrenciesRate(currency=currency.name, rate=currency.artist) for currency in currencies]


@router.post("/currency")
async def add_currencies(
        currency_rate: dto.CurrenciesRate, session: AsyncSession = Depends(db.get_session)
) -> dto.CurrenciesRate:
    currency = db.CurrenciesRate(name=currency_rate.currency, artist=currency_rate.rate)
    session.add(currency)
    await session.commit()
    await session.refresh(currency)
    return currency
