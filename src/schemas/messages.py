from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime
    is_read: bool = False


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    chat_id: Optional[int] = None
    sender_id: Optional[int] = None
    text: Optional[str] = None
    timestamp: Optional[datetime] = None
    is_read: Optional[bool] = None


class Message(MessageBase):
    id: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime
    is_read: bool

    class Config:
        from_attributes = True
