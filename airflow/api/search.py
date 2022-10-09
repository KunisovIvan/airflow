import asyncio
import json
import os
import uuid

import aioredis
import httpx
from fastapi import APIRouter

from airflow.models import dto
from airflow.settings import REDIS, APP
from airflow.utils import post_to_provider, convector

router = APIRouter()


@router.post(
    "/search",
    operation_id='postToProviders',
    summary='Get and save results from providers',
    response_model=dto.SearchRes
)
async def search() -> dto.SearchRes:
    search_id = str(uuid.uuid4())
    redis = await aioredis.from_url("redis://localhost", password=REDIS.PASS, db=REDIS.DB)
    #
    async with httpx.AsyncClient() as client:
        #
        tasks = []
        for url in APP.PROVIDER_URLS:
            tasks.append(asyncio.create_task(post_to_provider(url, client)))
        #
        for task in tasks:
            res = await task
            value = await redis.get(search_id)
            #
            data = dto.Results(search_id=search_id).prepare_to_redis(value=value, res=res.json())
            await redis.setex(search_id, 600, data.json())
    #
    value = await redis.get(search_id)
    data = dto.Results(search_id=search_id).set_status(value=value, status=dto.Status.completed)
    await redis.setex(search_id, 600, data.json())
    #
    return dto.SearchRes(search_id=search_id)


@router.get(
    "/results/{search_id}/{currency}",
    operation_id='getResult',
    summary='Get search results by search_id',
    response_model=dto.Results
)
async def results(search_id: str, currency: dto.Currency) -> dto.Results:
    redis = await aioredis.from_url("redis://localhost", password=os.getenv('REDIS_PASS'), db=1)
    value = await redis.get(search_id)
    currencies = await redis.get('currency')
    #
    if value:
        data = dto.Results.parse_raw(value)
        #
        for flights in data.items:
            current_currency = flights.pricing.currency
            if current_currency != currency:
                total = await convector(
                    summ=float(flights.pricing.total),
                    current=currency,
                    received=current_currency,
                    currencies=json.loads(currencies),
                )
                flights.pricing.total = total
                flights.pricing.currency = currency
        #
        data = data.sorted_by_price(reverse=True)
        #
        return dto.Results(search_id=search_id, status=data.status, items=data.items)
    #
    return dto.Results(search_id=search_id)
