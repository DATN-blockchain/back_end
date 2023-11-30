from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserInfo


class MessengerBase(BaseModel):
    id: Optional[str] = None
    sender_id: Optional[str] = None
    receiver_id: Optional[str] = None
    content: Optional[str] = None
    data: Optional[dict] = None
    is_read: Optional[bool] = None


class MessengerCreate(MessengerBase):
    pass


class MessengerCreateParam(BaseModel):
    receiver_id: str
    content: str


class MessengerUpdate(BaseModel):
    content: str


class MessengerResponse(MessengerBase):
    create_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    sender: Optional[UserInfo] = None
    receiver: Optional[UserInfo] = None
