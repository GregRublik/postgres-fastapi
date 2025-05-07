from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import json

import aio_pika
from config import settings

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import (
    User,
)
from exceptions import (
    ModelAlreadyExistsException,
    ModelNoFoundException,
    UserNoFoundException
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
    Репозиторий для работы с RabbitMQ
    """

    def __init__(self, connection_string: str = settings.rabbitmq.amqp_url):
        self.connection_string = connection_string
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None

    async def connect(self):
        """Установка соединения с RabbitMQ"""
        self.connection = await aio_pika.connect_robust(self.connection_string)
        self.channel = await self.connection.channel()

    async def close(self):
        """Закрытие соединения"""
        if self.connection:
            await self.connection.close()

    async def add_one(self, queue_name: str, message: Dict[str, Any], **kwargs):
        """
        Отправка сообщения в очередь RabbitMQ
        :param queue_name: Название очереди
        :param message: Сообщение для отправки (словарь)
        :param kwargs: Дополнительные параметры (durable, persistent и т.д.)
        """
        if not self.connection or not self.channel:
            await self.connect()

        queue = await self.channel.declare_queue(
            queue_name,
            durable=kwargs.get('durable', False)
        )

        message_body = json.dumps(message).encode()
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
                delivery_mode=kwargs.get('delivery_mode', 1)  # 1 - не persistent, 2 - persistent
            ),
            routing_key=queue_name
        )

    async def consume(self, queue_name: str, callback: callable, **kwargs):
        """
        Подписка на получение сообщений из очереди
        :param queue_name: Название очереди
        :param callback: Функция для обработки сообщений
        :param kwargs: Дополнительные параметры (durable, prefetch_count и т.д.)
        """
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
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        # Можно добавить логику повторной обработки или dead letter queue

    async def find_one(self, queue_name: str, timeout: int = 5) -> Optional[Dict[str, Any]]:
        """
        Получение одного сообщения из очереди с таймаутом
        :param queue_name: Название очереди
        :param timeout: Время ожидания сообщения в секундах
        :return: Сообщение или None, если очередь пуста
        """
        if not self.connection or not self.channel:
            await self.connect()

        queue = await self.channel.declare_queue(queue_name)

        try:
            message = await queue.get(timeout=timeout, fail=False)
            if message:
                await message.ack()
                return json.loads(message.body.decode())
        except aio_pika.exceptions.QueueEmpty:
            pass
        return None

    async def find_all(self, queue_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Получение нескольких сообщений из очереди
        :param queue_name: Название очереди
        :param limit: Максимальное количество сообщений
        :return: Список сообщений
        """
        if not self.connection or not self.channel:
            await self.connect()

        queue = await self.channel.declare_queue(queue_name)
        messages = []

        for _ in range(limit):
            message = await queue.get(fail=False)
            if not message:
                break
            await message.ack()
            messages.append(json.loads(message.body.decode()))

        return messages


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
