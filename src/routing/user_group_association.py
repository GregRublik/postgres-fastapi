from typing import Annotated

from fastapi import APIRouter, Depends

from depends import user_group_association_service
from schemas.user_group_association import UserGroupAssociationCreate
from services.user_group_association import UserGroupAssociationService

user_group_association = APIRouter(prefix="/user_group_association", tags=["user_group_association"])


@user_group_association.post("/add")
async def add_one(
        user_group_association: UserGroupAssociationCreate,
        user_group_association_service: Annotated[UserGroupAssociationService, Depends(user_group_association_service)]
):
    user_group_association_id = await user_group_association_service.add_user_group_association(user_group_association)
    return {"user_group_association_id": user_group_association_id}

# @main.post("/get_all")
# async def get_all(main: MainSchema, main_service: Annotated[MainService, Depends(main_service)]) -> MainSchema:
#    book = book_service.create_book()
#    return book
