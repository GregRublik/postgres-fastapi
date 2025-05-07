from pydantic import BaseModel
from typing import Optional


class MessageSchema(BaseModel):
    event_type: str
    payload: dict
    timestamp: Optional[float] = None
    metadata: Optional[dict] = None
