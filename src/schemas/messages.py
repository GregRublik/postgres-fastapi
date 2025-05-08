from pydantic import BaseModel
from typing import Optional


class MessageSchema(BaseModel):
    event_type: str
    payload: dict
    timestamp: Optional[float] = None
    metadata: Optional[dict] = None


class CreateMessage(BaseModel):
    queue_name: str = "first_message"
    message_name: str
    data: dict


class ReadMessage(BaseModel):
    queue_name: str = "first_message"
    timeout: int = 5

