import asyncio
import logging
from datetime import datetime

import httpx

from app.models import dto
from app.redis import AsyncRedisConnector
from app.settings import APP

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


async def search_(search_id: str):
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


async def post_to_provider(url: str, client: httpx.AsyncClient) -> httpx.Response:
    """Send post request to providers."""

    log.info(f"request :: url {url} :: time {datetime.now()}")
    res = await client.post(url + '/search', timeout=100)
    log.info(f"response :: url {url} :: time {datetime.now()}")
    return res


async def convector(summ: float, current: dto.Currency, received: dto.Currency, currencies: dict) -> float:
    heft = summ / currencies[current.value]
    return round(heft * currencies[received.value], 3)
