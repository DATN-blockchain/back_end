from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserInfo


class DetailDescriptionBase(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    product_id: Optional[str] = None


class DetailDescriptionCreateParams(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    product_id: Optional[str] = None


class DetailDescriptionCreate(DetailDescriptionBase):
    pass


class DetailDescriptionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class DetailDescriptionResponse(DetailDescriptionBase):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
