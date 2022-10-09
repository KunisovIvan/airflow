from celery import Celery
from celery.schedules import crontab

from app.utils import update_currency_

app = Celery()
app.config_from_object('celery_tasks.celeryconfig')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every day at 12:00 a.m.
    sender.add_periodic_task(crontab(hour=12, minute=0), update_currency.s())


@app.task
def update_currency():
    """Requests and saving exchange rates."""

    update_currency_()
