from abc import ABC, abstractmethod

from fastapi.params import Depends
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from config import logger

from db.database import async_session_maker, SessionDep

from db.models import (
    User,
)
from exeptions import (
    UserAlreadyExistsException,
    ModelAlreadyExistsException,
    ModelNoFoundException,
    UserNoFoundException
)


class AbstractRepository(ABC):
    """
    Aбстрактный репозиторий нужен чтобы при наследовании определяли его базовые методы работы с бд
    """
    model = None

    @abstractmethod
    async def add_one(self, data: dict, session: Depends(SessionDep)):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, data: dict, session: Depends(SessionDep)):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, session: Depends(SessionDep)):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    """
    Репозиторий для работы с sqlalchemy
    """
    model = None

    async def add_one(self, data: dict, session: Depends(SessionDep)):
        async with session() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            try:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar_one()
            except IntegrityError:
                raise ModelAlreadyExistsException

    async def find_all(self, session: Depends(SessionDep)):
        async with session() as session:
            stmt = select(self.model)
            try:
                res = await session.execute(stmt)
                return [row[0].to_read_model() for row in res.all()]
            except NoResultFound:
                raise ModelNoFoundException

    async def find_one(self, data: dict, session: Depends(SessionDep)):
        async with session() as session:
            stmt = select(self.model).where(**data)
            try:
                res = await session.execute(stmt)
                return res.scalar_one()
            except NoResultFound:
                raise ModelNoFoundException


class UserRepository(SQLAlchemyRepository):
    model = User

    async def find_one(self, data: dict, session: Depends(SessionDep)):
        async with session() as session:
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

    async def find_one_by_email(self, data: dict, session: Depends(SessionDep)):
        async with async_session_maker() as session:
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
