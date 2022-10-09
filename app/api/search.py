import asyncio
import json
import uuid

import httpx
from fastapi import APIRouter

from app.models import dto
from app.redis import AsyncRedisConnector
from app.settings import APP
from app.utils import post_to_provider, convector

router = APIRouter()


@router.post(
    "/search",
    operation_id='postToProviders',
    summary='Get and save results from providers',
    response_model=dto.SearchRes
)
async def search() -> dto.SearchRes:
    search_id = str(uuid.uuid4())
    redis = AsyncRedisConnector()
    await redis.connect()
    #
    async with httpx.AsyncClient() as client:
        #
        tasks = []
        for url in APP.PROVIDER_URLS:
            tasks.append(asyncio.create_task(post_to_provider(url, client)))
        #
        for task in tasks:
            res = await task
            value = await redis.get_key(search_id)
            #
            data = dto.Results(search_id=search_id).prepare_to_redis(value=value, res=res.json())
            await redis.set_key(search_id, data.json(), ttl=300)
    #
    value = await redis.get_key(search_id)
    data = dto.Results(search_id=search_id).set_status(value=value, status=dto.Status.completed)
    await redis.set_key(search_id, data.json(), ttl=300)
    #
    return dto.SearchRes(search_id=search_id)


@router.get(
    "/results/{search_id}/{currency}",
    operation_id='getResult',
    summary='Get search results by search_id',
    response_model=dto.Results
)
async def results(search_id: str, currency: dto.Currency) -> dto.Results:
    redis = AsyncRedisConnector()
    await redis.connect()
    value = await redis.get_key(search_id)
    currencies = await redis.get_key('currencies_rate')
    #
    if value and currencies:
        data = dto.Results.parse_obj(value)
        #
        for flights in data.items:
            current_currency = flights.pricing.currency
            if current_currency != currency:
                total = await convector(
                    summ=float(flights.pricing.total),
                    current=currency,
                    received=current_currency,
                    currencies=currencies,
                )
                flights.price = dto.Price(amount=str(total), currency=currency)
            else:
                flights.price = dto.Price(amount=flights.pricing.total, currency=currency)
        #
        data = data.sorted_by_price(reverse=True)
        #
        return dto.Results(search_id=search_id, status=data.status, items=data.items)
    #
    return dto.Results(search_id=search_id)
