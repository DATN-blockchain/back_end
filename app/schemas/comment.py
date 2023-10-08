from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.reply_comment import ReplyCommentResponse
from app.schemas.user import UserInfo


class CommentBase(BaseModel):
    content: Optional[str] = None
    marketplace_id: Optional[str] = None
    user_id: Optional[str] = None


class CommentCreateParams(BaseModel):
    content: str
    marketplace_id: str


class CommentCreate(CommentBase):
    id: str


class CommentUpdateParams(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    id: str


class CommentResponse(CommentBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    user: Optional[UserInfo] = None
    reply_comments: List[ReplyCommentResponse] = None
