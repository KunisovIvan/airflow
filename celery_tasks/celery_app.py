import json
from datetime import datetime

import requests
import xmltodict
from celery import Celery
from app import redis
from celery.schedules import crontab

from app.settings import APP, REDIS

app = Celery()
app.config_from_object('celery_tasks.celeryconfig')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every day at 12:00 a.m.
    sender.add_periodic_task(crontab(hour=12, minute=0), update_currency.s())


@app.task
def update_currency():
    r = redis.Redis(host=REDIS.HOST, port=REDIS.PORT, db=REDIS.DB, password=REDIS.PASS)
    url = f"{APP.CURRENCY_URL}{datetime.now().strftime('%d.%m.%Y')}"
    res = requests.get(url)
    dict_data = xmltodict.parse(res.content)
    currencies = dict_data.get('rates').get('item')
    currencies = {c['title']: float(c['description']) for c in currencies}
    currencies['KZT'] = 1.0
    r.set("currencies_rate", json.dumps(currencies))
