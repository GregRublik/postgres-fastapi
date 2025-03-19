from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from db.database import async_session_maker

from db.models import (
    User,
    # UserGroupAssociation,
    # Chat,
    # Group,
    # Message
)


class AbstractRepository(ABC):
    """
    Aбстрактный репозиторий нужен чтобы при наследовании определяли его базовые методы работы с бд
    """
    model = None

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """
    Репозиторий для работы с sqlalchemy
    """
    model = None

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self):
        async with async_session_maker() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return [row[0].to_read_model() for row in res.all()]

    async def find_one(self, data: dict):
        async with async_session_maker() as session:
            stmt = select(self.model).where(**data)
            res = await session.execute(stmt)
            return res.one()


# class MainRepository(SQLAlchemyRepository):
#     model = Main


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_one(self, data: dict):
        async with async_session_maker() as session:
            stmt = (
                select(self.model)
                .where(self.model.email == data['email'])
                .limit(limit=1)
            )
            res = await session.execute(stmt)
            return res.one()


# class UserGroupAssociationRepository(SQLAlchemyRepository):
#     model = UserGroupAssociation
#
#
# class ChatRepository(SQLAlchemyRepository):
#     model = Chat
#
#
# class GroupRepository(SQLAlchemyRepository):
#     model = Group
#
#
# class MessageRepository(SQLAlchemyRepository):
#     model = Message
#
#     async def find_all(self, data: dict):
#         async with async_session_maker() as session:
#             stmt = (
#                 select(self.model)
#                 .where(self.model.chat_id == data['chat_id'])
#                 .limit(data['limit'])
#                 .offset(data['offset'])
#                 .order_by(self.model.timestamp.asc())
#             )
#             res = await session.execute(stmt)
#             return [row[0].to_read_model() for row in res.all()]
