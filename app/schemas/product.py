from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..model.base import ProductType, ProductStatus
from app.schemas.user import UserInfo


class ProductBase(BaseModel):
    id: Optional[str] = None
    product_type: Optional[ProductType] = None
    product_status: Optional[ProductStatus] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    number_of_sales: Optional[int] = None
    is_sale: Optional[bool] = None
    banner: Optional[str] = None
    created_by: Optional[str] = None


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


class ProductResponseChart(ProductBase):
    project_chart: Optional[dict] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProductResponse(ProductBase):
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    user: Optional[UserInfo] = None
