import uuid

from fastapi import APIRouter
from fastapi import BackgroundTasks

from app.models import dto
from app.base_redis import AsyncRedisConnector
from app.utils import convector, search_

router = APIRouter()


@router.post(
    "/search",
    operation_id='postToProviders',
    summary='Get and save results from providers',
    response_model=dto.SearchRes
)
async def search(background_tasks: BackgroundTasks) -> dto.SearchRes:
    search_id = str(uuid.uuid4())
    background_tasks.add_task(search_, search_id)
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
