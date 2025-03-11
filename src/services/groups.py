from repositories.repository import AbstractRepository
from schemas.groups import GroupCreate, Group


class GroupService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add_group(self, group: GroupCreate):
        group_dict = group.model_dump()
        group_id = await self.repository.add_one(group_dict)
        return group_id

    async def find_all(self, group: Group):
        result = self.repository.find_all()
        return result
