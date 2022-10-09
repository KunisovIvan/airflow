import logging
from datetime import datetime

import httpx

from airflow.models import dto

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


async def post_to_provider(url: str, client: httpx.AsyncClient) -> httpx.Response:
    """Send post request to providers."""

    log.info(f"request :: url {url} :: time {datetime.now()}")
    res = await client.post(url + '/search', timeout=100)
    log.info(f"response :: url {url} :: time {datetime.now()}")
    return res


async def convector(summ: float, current: dto.Currency, received: dto.Currency, currencies: dict) -> float:
    heft = summ / currencies[current.value]
    return round(heft * currencies[received.value], 3)
