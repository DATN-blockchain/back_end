from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.product import ProductResponse


class GrowUpBase(BaseModel):
    id: Optional[str] = None
    product_farmer_id: Optional[str] = None
    description: Optional[str] = None
    image: Optional[int] = None
    video: Optional[int] = None
    hashed_data: Optional[int] = None


class GrowUpCreate(GrowUpBase):
    pass


class GrowUpCreateParam(GrowUpBase):
    product_farmer_id: Optional[str] = None
    description: Optional[str] = None
    image: Optional[int] = None
    video: Optional[int] = None


class GrowUpUpdate(BaseModel):
    hashed_data: Optional[int] = None


class GrowUpResponse(GrowUpBase):
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    # product: Optional[ProductResponse] = None
