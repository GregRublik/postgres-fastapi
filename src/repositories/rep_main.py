from db.models import Main
from repositories.repository import SQLAlchemyRepository


class MainRepository(SQLAlchemyRepository):
    model = Main
