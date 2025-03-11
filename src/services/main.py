# from repositories.repository import AbstractRepository
# from schemas.main import MainSchema
#
#
# class MainService:
#
#     def __init__(self, repository: AbstractRepository):
#         self.repository: AbstractRepository = repository()
#
#     async def add_chat(self, main: MainSchema):
#         main_dict = main.model_dump()
#         main_id = await self.repository.add_one(main_dict)
#         return main_id
#
#     async def find_all(self, main: MainSchema):
#         result = self.repository.find_all()
#         return result
