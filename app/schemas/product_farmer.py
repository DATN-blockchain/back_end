from typing import Optional

from pydantic import BaseModel

from app.schemas import ProductResponse
from app.schemas.transaction_sf import TransactionSFResponse


class ProductFarmerBase(BaseModel):
    id: str
    product_id: str
    transaction_sf_id: str


class ProductFarmerCreate(ProductFarmerBase):
    pass


class ProductFarmerUpdate(BaseModel):
    pass


class ProductFarmerHistoryResponse(ProductFarmerBase):
    product: Optional[ProductResponse] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    transactions_sf: Optional[TransactionSFResponse] = None
