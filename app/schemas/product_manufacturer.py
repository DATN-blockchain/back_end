from typing import Optional

from pydantic import BaseModel

from app.schemas import ProductResponse
from app.schemas.transaction_fm import TransactionFMResponse


class ProductManufacturerBase(BaseModel):
    id: str
    product_id: str
    transaction_fm_id: str


class ProductManufacturerCreate(ProductManufacturerBase):
    pass


class ProductManufacturerUpdate(BaseModel):
    pass


class ProductManufacturerHistoryResponse(ProductManufacturerBase):
    product: Optional[ProductResponse] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    transactions_fm: Optional[TransactionFMResponse] = None
