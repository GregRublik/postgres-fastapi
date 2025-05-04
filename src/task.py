from celery import Celery
from config import settings

app = Celery('worker', broker=settings.redis.redis_url)


@app.task
def hello_world():
    return 'Hello World!'
