from abc import ABC, abstractmethod
import datetime
from typing import Optional, List, Dict, Any
import json

from uuid import uuid4

import aio_pika
from aio_pika import DeliveryMode
from aio_pika.exceptions import (
    AMQPConnectionError,
    ChannelClosed,
    QueueEmpty,
    DeliveryError
)

from config import settings
from schemas.messages import CreateMessage

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import (
    User,
)

from exceptions import (
    ModelAlreadyExistsException,
    ModelNoFoundException,
    UserNoFoundException,
    MessagePublishException,
    MessageConsumeException,
    QueueEmptyException,
    BrokerConnectionException
)


class AbstractRepository(ABC):
    """
    Абстрактный репозиторий нужен чтобы при наследовании определяли его базовые методы работы с бд
    """
    model = None

    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, *args, **kwargs):
        raise NotImplementedError


class RabbitMQRepository(AbstractRepository):
    """
    Репозиторий для работы с RabbitMQ с полной обработкой исключений
    """

    def __init__(self, connection_string: str = settings.rabbitmq.amqp_url):
        self.connection_string = connection_string
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None

    async def connect(self):
        """Установка соединения с RabbitMQ"""
        try:
            self.connection = await aio_pika.connect_robust(self.connection_string)
            self.channel = await self.connection.channel()
        except AMQPConnectionError as e:
            raise BrokerConnectionException(f"Failed to connect to RabbitMQ: {str(e)}")
        except Exception as e:
            raise BrokerConnectionException(f"Unexpected connection error: {str(e)}")

    async def close(self):
        """Закрытие соединения"""
        try:
            if self.connection:
                await self.connection.close()
        except Exception as e:
            # Логируем ошибку закрытия, но не пробрасываем исключение
            print(f"Error closing RabbitMQ connection: {str(e)}")

    async def add_one(self, message: CreateMessage):
        """
        Отправка сообщения в очередь RabbitMQ
        :param message: Содержит queue_name, message_name, data
        :raises: MessagePublishException при ошибке публикации
        """
        try:
            if not self.connection or not self.channel:
                await self.connect()

            # Создаем очередь если она еще не создана
            queue = await self.channel.declare_queue(
                message.queue_name,
                durable=True,
                auto_delete=False,
                arguments={
                    'x-ha-policy': 'all'
                }
            )

            # Формируем тип сообщения
            new_message = {
                'task': message.message_name,
                'id': str(uuid4()),
                'args': [message.data],
                'kwargs': {}
            }

            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(new_message).encode(),
                    content_type='application/json',
                    delivery_mode=2,  # Persistent
                    content_encoding='utf-8',
                    headers={
                        'task': message.message_name,
                        'id': new_message['id']
                    }
                ),
                routing_key=message.queue_name
            )
        except Exception as e:
            raise MessagePublishException(f"Failed to publish message: {str(e)}")
        finally:
            await self.close()

    async def consume(self, queue_name: str, callback: callable, **kwargs):
        """
        Подписка на получение сообщений из очереди
        :param queue_name: Название очереди
        :param callback: Функция для обработки сообщений
        :param kwargs: Дополнительные параметры
        :raises: MessageConsumeException при ошибке потребления
        """
        try:
            if not self.connection or not self.channel:
                await self.connect()

            queue = await self.channel.declare_queue(
                queue_name,
                durable=kwargs.get('durable', False)
            )

            if 'prefetch_count' in kwargs:
                await self.channel.set_qos(prefetch_count=kwargs['prefetch_count'])

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        try:
                            message_body = json.loads(message.body.decode())
                            await callback(message_body)
                        except json.JSONDecodeError:
                            await message.reject(requeue=False)
                            print(f"Invalid JSON message in queue {queue_name}")
                        except Exception as e:
                            await message.reject(requeue=True)
                            print(f"Error processing message: {str(e)}")
        except QueueEmpty:
            raise QueueEmptyException(f"Queue {queue_name} is empty")
        except ChannelClosed as e:
            raise MessageConsumeException(f"Channel error: {str(e)}")
        except Exception as e:
            raise MessageConsumeException(f"Failed to consume messages: {str(e)}")

    async def find_one(self, queue_name: str, timeout: int = 5) -> Optional[Dict[str, Any]]:
        """
        Получение одного сообщения из очереди
        :param queue_name: Название очереди
        :param timeout: Время ожидания сообщения
        :return: Сообщение или None
        :raises: QueueEmptyException если очередь пуста
        :raises: MessageConsumeException при других ошибках
        """
        try:
            if not self.connection or not self.channel:
                await self.connect()

            queue = await self.channel.declare_queue(queue_name, durable=True)
            message = await queue.get(timeout=timeout, fail=False)

            if not message:
                raise QueueEmptyException(f"Queue {queue_name} is empty")

            await message.ack()
            return json.loads(message.body.decode())
        except QueueEmpty:
            raise QueueEmptyException(f"Queue {queue_name} is empty")
        except json.JSONDecodeError:
            await message.ack()  # todo на данный момент сделано так чтобы оно подтверждалось как прочитанное
                                # todo но наверное лучше возвращать ее обратно в очередь, либо помечать как ошибочное
            raise MessageConsumeException("Invalid JSON message format")
        except Exception as e:
            raise MessageConsumeException(f"Failed to get message: {str(e)}")

    async def find_all(self, queue_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Получение нескольких сообщений из очереди
        :param queue_name: Название очереди
        :param limit: Максимальное количество сообщений
        :return: Список сообщений
        :raises: MessageConsumeException при ошибках
        """
        try:
            if not self.connection or not self.channel:
                await self.connect()

            queue = await self.channel.declare_queue(queue_name)
            messages = []

            for _ in range(limit):
                message = await queue.get(fail=False)
                if not message:
                    break

                try:
                    await message.ack()
                    messages.append(json.loads(message.body.decode()))
                except json.JSONDecodeError:
                    print(f"Invalid JSON message skipped in queue {queue_name}")
                    continue

            return messages
        except Exception as e:
            raise MessageConsumeException(f"Failed to get messages: {str(e)}")


class RedisRepository(AbstractRepository):
    """
    Репозиторий для работы с RabbitMQ
    """
    model = None

    @abstractmethod
    async def add_one(self, session: AsyncSession, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, session: AsyncSession, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, session: AsyncSession):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """
    Репозиторий для работы с sqlalchemy
    """
    model = None

    async def add_one(self, session: AsyncSession, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        try:
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
        except IntegrityError:
            raise ModelAlreadyExistsException

    async def find_all(self, session: AsyncSession):
        stmt = select(self.model)
        try:
            res = await session.execute(stmt)
            return [row[0].to_read_model() for row in res.all()]
        except NoResultFound:
            raise ModelNoFoundException

    async def find_one(self, session: AsyncSession, data: dict):
        stmt = select(self.model).where(**data)
        try:
            res = await session.execute(stmt)
            return res.scalar_one()
        except NoResultFound:
            raise ModelNoFoundException


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_one(self, session: AsyncSession, data: dict):
        stmt = (
            select(self.model)
            .where(self.model.id == data['id'])
            .limit(limit=1)
        )
        try:
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
        except NoResultFound:
            raise UserNoFoundException('User is not exist')

    async def find_one_by_email(self, session: AsyncSession, data: dict):
        stmt = (
            select(self.model)
            .where(self.model.email == data['email'])
            .limit(limit=1)
        )
        try:
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()
        except NoResultFound:
            raise UserNoFoundException('User is not exist')
