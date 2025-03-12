from repositories.repository import AbstractRepository
from schemas.user_group_association import UserGroupAssociationCreate, UserGroupAssociation


class UserGroupAssociationService:

    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository()

    async def add_user_group_association(self, user_group_association: UserGroupAssociationCreate):
        group_dict = user_group_association.model_dump()
        group_id = await self.repository.add_one(group_dict)
        return group_id

    # async def find_all(self, user_group_association: UserGroupAssociation):
    #     result = self.repository.find_all()
    #     return result
