from typing import Annotated

from fastapi import APIRouter, Depends

from depends import groups_service
from schemas.groups import GroupCreate
from services.groups import GroupService

groups = APIRouter(prefix="/groups", tags=["groups"])


@groups.post("/add")
async def add_one(
        group: GroupCreate,
        group_service: Annotated[GroupService, Depends(groups_service)]
):
   group_id = await group_service.add_group(group)
   return {"group_id": group_id}


# @main.post("/get_all")
# async def get_all(main: MainSchema, main_service: Annotated[MainService, Depends(main_service)]) -> MainSchema:
#    book = book_service.create_book()
#    return book
