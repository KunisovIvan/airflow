import asyncio
from datetime import datetime

import requests
import xmltodict
from celery import Celery
from sqlmodel.orm import session

from airflow.api.db import add_currencies
from airflow.models import dto
from airflow.settings import APP

app = Celery()
app.config_from_object('celeryconfig')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(10.0, update_currency.s())

    # Executes every day at 12:00 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=12, minute=00),
    #     update_currency.s(),
    # )


async def async_task():
    await asyncio.sleep(5)


@app.task
def update_currency():
    url = f"{APP.CURRENCY_URL}{datetime.now().strftime('%d.%m.%Y')}"
    res = requests.get(url)
    dict_data = xmltodict.parse(res.content)
    currencies = dict_data.get('rates').get('item')
    currencies = {c['title']: float(c['description']) for c in currencies}
    currencies['KZT'] = 1.0
    c = dto.CurrenciesRate(currency='KZT', rate=44.56)
    asyncio.run(add_currencies(c))
