from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from db.database import session_manager

from db.models import User, UserGroupAssociation, Chat, Group, Message


class AbstractRepository(ABC):
    """
    Aбстрактный репозиторий нужен чтобы при наследовании определяли его базовые методы работы с бд
    """
    @abstractmethod
    async def add_one(*args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_all(*args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_history(*args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """
    Репозиторий для работы с sqlalchemy
    """
    model = None

    @session_manager
    async def add_one(self, session: AsyncSession, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()

    @session_manager
    async def find_all(self, session: AsyncSession):
        stmt = select(self.model)
        res = await session.execute(stmt)
        return [row[0].to_read_model() for row in res.all()]


# class MainRepository(SQLAlchemyRepository):
#     model = Main


class UserRepository(SQLAlchemyRepository):
    model = User


class UserGroupAssociationRepository(SQLAlchemyRepository):
    model = UserGroupAssociation


class ChatRepository(SQLAlchemyRepository):
    model = Chat


class GroupRepository(SQLAlchemyRepository):
    model = Group


class MessageRepository(SQLAlchemyRepository):
    model = Message

    @session_manager
    async def find_all(self, session: AsyncSession, data: dict):
        stmt = (
            select(Message)
            .where(Message.chat_id == data['chat_id'])
            .limit(data['limit'])
            .offset(data['offset'])
            .order_by(Message.timestamp.asc())
        )
        res = await session.execute(stmt)
        return [row[0].to_read_model() for row in res.all()]
