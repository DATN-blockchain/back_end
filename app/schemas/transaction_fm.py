from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import UserInfo
from app.schemas.product import ProductResponse


class TransactionFMBase(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    user_id: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    tx_hash: Optional[int] = None
    status: Optional[int] = None


class TransactionFMCreate(TransactionFMBase):
    pass


class TransactionFMUpdate(BaseModel):
    tx_hash: Optional[int] = None
    status: Optional[int] = None


class TransactionFMResponse(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    user_id: Optional[str] = None
    status: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    product: Optional[ProductResponse] = None
    user: Optional[UserInfo] = None
