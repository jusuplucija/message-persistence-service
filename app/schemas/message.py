from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, UUID4


class RoleEnum(str, Enum):
    ai = "ai"
    user = "user"


class MessageCreate(BaseModel):
    message_id: UUID4
    chat_id: UUID4
    content: str
    rating: bool
    sent_at: datetime
    role: RoleEnum


class MessageUpdate(BaseModel):
    content: str | None = None
    rating: bool | None = None
    sent_at: datetime | None = None
    role: RoleEnum | None = None


class MessageRead(BaseModel):
    message_id: UUID4
    chat_id: UUID4
    content: str
    rating: bool
    sent_at: datetime
    role: RoleEnum

    model_config = ConfigDict(from_attributes=True)