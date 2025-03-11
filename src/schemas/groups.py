from typing import Optional
from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    creator_id: int


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    creator_id: Optional[int] = None


class Group(GroupBase):
    id: int

    class Config:
        from_attributes = True
