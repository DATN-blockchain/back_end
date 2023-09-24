from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import ProductResponse


class TransactionSFBase(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    user_id: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    hashed_data: Optional[int] = None
    status: Optional[int] = None


class TransactionSFCreate(TransactionSFBase):
    pass


class TransactionSFUpdate(BaseModel):
    hashed_data: Optional[int] = None
    status: Optional[int] = None


class TransactionSFResponse(BaseModel):
    product_id: Optional[str] = None
    user_id: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    product: Optional[ProductResponse] = None
