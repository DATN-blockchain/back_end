from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from . import ProductResponse
from ..model.base import ProductType
from app.schemas.user import UserInfo


class MarketplaceBase(BaseModel):
    id: str
    order_type: Optional[ProductType] = None
    order_id: Optional[str] = None
    order_by: Optional[str] = None
    hash_data: Optional[str] = None


class MarketplaceCreate(BaseModel):
    id: str
    order_type: Optional[ProductType] = None
    order_id: Optional[str] = None
    order_by: Optional[str] = None


class MarketplaceUpdate(BaseModel):
    hash_data: Optional[str] = None


class MarketplaceResponse(MarketplaceBase):
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    product: Optional[ProductResponse] = None