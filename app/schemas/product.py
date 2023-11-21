from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.detail_description import DetailDescriptionResponse
from app.schemas.classify_goods import ClassifyGoodsResponse
from ..model.base import ProductType, ProductStatus
from app.schemas.user import UserInfo


class ProductBase(BaseModel):
    id: Optional[str] = None
    product_type: Optional[ProductType] = None
    product_status: Optional[ProductStatus] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    last_price: Optional[int] = None
    quantity: Optional[int] = None
    number_of_sales: Optional[int] = None
    is_sale: Optional[bool] = None
    banner: Optional[str] = None
    created_by: Optional[str] = None
    tx_hash: Optional[str] = None
    view: Optional[int] = None


class ProductCreateParams(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[int] = None
    last_price: Optional[int] = None
    quantity: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    banner: Optional[str] = None
    price: Optional[int] = None
    last_price: Optional[int] = None
    quantity: Optional[int] = None
    tx_hash: Optional[str] = None
    data: Optional[dict] = None


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

    detail_description: Optional[list[DetailDescriptionResponse]] = None
    classify_goods: Optional[list[ClassifyGoodsResponse]] = None
    user: Optional[UserInfo] = None


class ProductResponseDetail(ProductBase):
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    detail_description: Optional[DetailDescriptionResponse] = None
    user: Optional[UserInfo] = None
