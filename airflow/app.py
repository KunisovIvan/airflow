from fastapi import FastAPI

from airflow.api import search, db
from airflow.models.db import init_db

from airflow.models.db import CurrenciesRate

app = FastAPI(title='Async AirFlow Service')
app.include_router(search.router, prefix='/api/v1/search', tags=['search'])
app.include_router(db.router, prefix='/api/v1/db', tags=['db'])


@app.on_event("startup")
async def on_startup():
    await init_db()
