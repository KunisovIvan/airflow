from fastapi import FastAPI

from airflow.api import search, db


app = FastAPI(title='Async AirFlow Service')
app.include_router(search.router)
app.include_router(db.router, prefix='/api/v1/db', tags=['db'])
