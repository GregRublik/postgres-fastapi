from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db_session
from repositories.repository import (
    UserRepository,
    RabbitMQRepository
    )
from services import users, jwt_services, broker


def get_jwt_service():
    return jwt_services.JWTService()


def get_user_repository() -> UserRepository:
    return UserRepository()


def get_user_service(
    session: AsyncSession = Depends(get_db_session),
    repository: UserRepository = Depends(get_user_repository)
) -> users.UserService:
    return users.UserService(repository, session)


def get_rabbitmq_repository() -> RabbitMQRepository:
    return RabbitMQRepository()  # connection_string


def get_broker_service(
        repository: RabbitMQRepository = Depends(get_rabbitmq_repository),
) -> broker.BrokerService:
    return broker.BrokerService(repository)
