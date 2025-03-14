from typing import Annotated

from fastapi import APIRouter, Depends

# from depends import main_service
# from schemas.main import MainSchema
# from services.main import MainService

main = APIRouter(tags=["main"])


@main.get("/")
async def index(
        main: MainSchema,
        main_service: Annotated[MainService, Depends(main_service)]
):
   main_id = await main_service.add_main(main)
   return {"task_id": main_id}


# @main.post("/get_all")
# async def get_all(main: MainSchema, main_service: Annotated[MainService, Depends(main_service)]) -> MainSchema:
#    book = book_service.create_book()
#    return book
