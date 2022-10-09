from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import db, dto

router = APIRouter()


@router.get("/", response_model=List[dto.CurrenciesRate])
async def get_currencies(session: AsyncSession = Depends(db.get_session)) -> List[dto.CurrenciesRate]:
    result = await session.execute(select(db.CurrenciesRate))
    currencies = result.scalars().all()
    return [dto.CurrenciesRate(currency=c.currency, rate=c.rate) for c in currencies]


@router.post("/")
async def add_currencies(
        currency_rate: dto.CurrenciesRate, session: AsyncSession = Depends(db.get_session)
) -> dto.CurrenciesRate:
    currency = db.CurrenciesRate(currency=currency_rate.currency, rate=currency_rate.rate)
    session.add(currency)
    await session.commit()
    await session.refresh(currency)
    return currency
