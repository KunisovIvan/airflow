from functools import partial

from fastapi import FastAPI

from app.api import search, currency
from app.base_redis import AsyncRedisConnector


async def setup_connectors(app: FastAPI):
    redis_connector = AsyncRedisConnector()
    await redis_connector.connect()
    app.state.redis = redis_connector


app = FastAPI(title='Async AirFlow Service')
app.include_router(search.router)
app.include_router(currency.router, prefix='/api/v1/currency', tags=['currency'])
app.add_event_handler(event_type='startup', func=partial(setup_connectors, app=app))
