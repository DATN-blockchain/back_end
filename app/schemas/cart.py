from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.product import ProductResponse
from app.schemas.user import UserInfo


class CartBase(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    user_id: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None


class CartCreate(CartBase):
    pass


class CartCreateParam(BaseModel):
    product_id: str
    price: int
    quantity: int


class CartUpdate(BaseModel):
    pass


class CartResponse(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    user_id: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    product: Optional[ProductResponse] = None
    user: Optional[UserInfo] = None
