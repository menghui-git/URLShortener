from celery.schedules import crontab

from shortener.models import URL
from URLShortener.celery import app


@app.task(name='delete_expired_urls')
def delete_expired_urls():
    URL.objects.delete_expired_urls()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Daily task
    sender.add_periodic_task(crontab(hour=0, minute=0),
                             delete_expired_urls.s(),
                             name='Delete expired url data')