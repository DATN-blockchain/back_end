from typing import Optional

from pydantic import BaseModel


class ClassifyGoodsBase(BaseModel):
    id: Optional[str] = None
    product_id: Optional[str] = None
    data: Optional[dict] = None


class ClassifyGoodsCreate(ClassifyGoodsBase):
    pass


class ClassifyGoodsCreateParam(BaseModel):
    data: dict


class ClassifyGoodsUpdate(BaseModel):
    data: dict


class ClassifyGoodsResponse(ClassifyGoodsBase):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
