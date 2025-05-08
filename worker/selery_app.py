from celery import Celery
from config import settings

app = Celery(
    'tasks',
    broker=f'amqp://{settings.rabbitmq.rabbitmq_user}:{settings.rabbitmq.rabbitmq_password}@rabbitmq:5672//',
    backend=f'redis://:{settings.redis.redis_password}@{settings.redis.redis_host}:{settings.redis.redis_port}/0'
)

app.conf.task_routes = {
    'tasks.process_message': {'queue': 'first_message'},
}

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    worker_accept_content=['json'],
    event_serializer='json',
    task_compression='gzip',
    task_queues={
        'first_message': {
            'exchange': 'first_message',
            'exchange_type': 'direct',
            'routing_key': 'first_message',
            'durable': True
        }
    }
)
