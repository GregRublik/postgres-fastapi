from pydantic import BaseModel
from typing import Optional


class UserGroupAssociationBase(BaseModel):
    user_id: int
    group_id: int


class UserGroupAssociationCreate(UserGroupAssociationBase):
    pass


class UserGroupAssociationUpdate(BaseModel):
    user_id: Optional[int] = None
    group_id: Optional[int] = None


class UserGroupAssociation(UserGroupAssociationBase):
    class Config:
        from_attributes = True
