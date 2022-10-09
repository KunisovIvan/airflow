from fastapi import FastAPI

from app.api import search, currency

app = FastAPI(title='Async AirFlow Service')
app.include_router(search.router)
app.include_router(currency.router, prefix='/api/v1/currency', tags=['currency'])
