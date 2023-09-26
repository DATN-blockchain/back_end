from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from . import ProductResponse
from ..model.base import ProductType
from app.schemas.user import UserInfo


class ProductFarmerBase(BaseModel):
    id: str
    product_id: str
    transaction_sf_id: str


class ProductFarmerCreate(ProductFarmerBase):
    pass


class ProductFarmerUpdate(BaseModel):
    pass

# class ProductFarmerResponse(ProductFarmerBase):
#     created_at: Optional[datetime] = None
#
#     class Config:
#         orm_mode = True
#         arbitrary_types_allowed = True
#
#     product: Optional[ProductResponse] = None
