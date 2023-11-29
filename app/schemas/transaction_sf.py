from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import UserInfo, ProductHistoryResponse
from app.schemas.product import ProductResponse


class TransactionSFBase(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    user_id: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    tx_hash: Optional[str] = None
    status: Optional[str] = None
    receiver: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    order_by: Optional[str] = None


class TransactionSFCreate(TransactionSFBase):
    pass


class TransactionSFUpdate(BaseModel):
    tx_hash: Optional[str] = None
    status: Optional[str] = None


class TransactionSFResponse(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    user_id: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    receiver: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tx_hash: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    product: Optional[ProductResponse] = None
    user: Optional[UserInfo] = None


class TransactionSFHistoryResponse(TransactionSFBase):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    product: Optional[ProductHistoryResponse] = None
    user: Optional[UserInfo] = None
