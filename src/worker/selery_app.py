from celery import Celery
from config import settings

app = Celery(
    'tasks',
    broker=f'amqp://{settings.rabbitmq.rabbitmq_user}:{settings.rabbitmq.rabbitmq_password}@rabbitmq:5672//',
    backend=f'redis://:{settings.redis.redis_password}@{settings.redis.redis_host}:{settings.redis.redis_port}/0'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)
