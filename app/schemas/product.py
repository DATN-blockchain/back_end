from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from ..model.base import ProductType, ProductStatus
from app.schemas.user import UserInfo


class ProductBase(BaseModel):
    id: str
    product_type: Optional[ProductType] = None
    product_status: Optional[ProductStatus] = None
    name: str
    description: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None
    banner: Optional[str] = None
    created_by: str


class ProductCreateParams(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    banner: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None
    hashed_data: Optional[str] = None


class ProductResponse(ProductBase):
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    user: Optional[UserInfo] = None
