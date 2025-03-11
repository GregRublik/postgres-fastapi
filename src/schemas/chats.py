from pydantic import BaseModel
from typing import Optional


class ChatBase(BaseModel):
    name: str
    type: str  # 'personal' или 'group'


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None


class Chat(ChatBase):
    id: int

    class Config:
        from_attributes = True
