from typing import Union, Dict, Any, Optional, List
from repositories.repository import AbstractRepository, RabbitMQRepository
from schemas.messages import MessageSchema, ReadMessage  # Предположим, что у вас есть схема для сообщений
from exceptions import (
    MessagePublishException,
    MessageConsumeException,
    QueueEmptyException
)


class BrokerService:
    """
    Сервис для работы с брокером сообщений (RabbitMQ)
    """
    def __init__(self, repository: Union[AbstractRepository, RabbitMQRepository]):
        self.repository = repository

    async def publish_message(self, queue_name: str, message: Dict[str, Any], **kwargs) -> bool:
        """
        Публикация сообщения в очередь
        :param queue_name: Название очереди
        :param message: Сообщение для отправки
        :param kwargs: Дополнительные параметры (durable, persistent и т.д.)
        :return: True если сообщение успешно отправлено
        :raises: MessagePublishException при ошибке публикации
        """
        try:
            await self.repository.add_one(queue_name, message, **kwargs)
            return True
        except Exception as e:
            raise MessagePublishException(f"Failed to publish message: {str(e)}")

    async def get_single_message(self, mess: ReadMessage) -> Optional[Dict[str, Any]]:
        """
        Получение одного сообщения из очереди
        :param mess: Содержание сообщения
        :return: Сообщение или None если очередь пуста
        :raises: MessageConsumeException при ошибке получения
        """
        try:
            message = await self.repository.find_one(mess.queue_name, timeout=mess.timeout)
            if message is None:
                raise QueueEmptyException(f"Queue {mess.queue_name} is empty")
            return message
        except QueueEmptyException:
            raise
        except Exception as e:
            raise MessageConsumeException(f"Failed to consume message: {str(e)}")

    async def get_multiple_messages(self, queue_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Получение нескольких сообщений из очереди
        :param queue_name: Название очереди
        :param limit: Максимальное количество сообщений
        :return: Список сообщений
        :raises: MessageConsumeException при ошибке получения
        """
        try:
            messages = await self.repository.find_all(queue_name, limit=limit)
            if not messages:
                raise QueueEmptyException(f"Queue {queue_name} is empty")
            return messages
        except QueueEmptyException:
            raise
        except Exception as e:
            raise MessageConsumeException(f"Failed to consume messages: {str(e)}")

    async def consume_messages(self, queue_name: str, callback: callable, **kwargs):
        """
        Подписка на получение сообщений из очереди с callback обработчиком
        :param queue_name: Название очереди
        :param callback: Функция для обработки сообщений
        :param kwargs: Дополнительные параметры (prefetch_count и т.д.)
        :raises: MessageConsumeException при ошибке подписки
        """
        try:
            await self.repository.consume(
                queue_name=queue_name,
                callback=callback,
                **kwargs
            )
        except Exception as e:
            raise MessageConsumeException(f"Failed to start message consumer: {str(e)}")

    async def publish_validated_message(self, queue_name: str, message_data: Dict[str, Any], **kwargs) -> bool:
        """
        Публикация сообщения с валидацией по схеме
        :param queue_name: Название очереди
        :param message_data: Данные сообщения
        :param kwargs: Дополнительные параметры
        :return: True если сообщение успешно отправлено
        :raises: MessagePublishException при ошибке валидации или публикации
        """
        try:
            # Валидация сообщения по схеме
            validated_message = MessageSchema(**message_data).model_dump()
            return await self.publish_message(queue_name, validated_message, **kwargs)
        except ValueError as e:
            raise MessagePublishException(f"Message validation failed: {str(e)}")
        except Exception as e:
            raise MessagePublishException(f"Failed to publish validated message: {str(e)}")
