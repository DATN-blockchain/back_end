from typing import Optional

from pydantic import BaseModel

from app.schemas import UserInfo


class NotificationBase(BaseModel):
    id: str
    data: dict
    user_id: Optional[str] = None
    notification_type: str


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass


class NotificationResponse(BaseModel):
    data: Optional[dict] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    user: Optional[UserInfo] = None
