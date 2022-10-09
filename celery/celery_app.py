from datetime import datetime

import requests
import xmltodict

from celery import Celery
from celery.schedules import crontab

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


@app.task
def update_currency():
    url = f"{APP.CURRENCY_URL}{datetime.now().strftime('%d.%m.%Y')}"
    res = requests.get(url)
    dict_data = xmltodict.parse(res.content)
    currencies = dict_data.get('rates').get('item')
    currencies = {c['title']: float(c['description']) for c in currencies}
    currencies['KZT'] = 1.0
    # redis = await aioredis.from_url("redis://localhost", password='q1w2e3r4', db=1)
    # await redis.set('currency', json.dumps(currencies))
