import logging
import uuid

from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import CRUDBase
from ..model import GrowUp, Product
from ..model.base import ProductType, ProductStatus

from ..schemas import GrowUpCreate, GrowUpUpdate

logger = logging.getLogger(__name__)


class CRUDGrowUp(CRUDBase[GrowUp, GrowUpCreate, GrowUpUpdate]):
    @staticmethod
    def get_grow_up_by_id(db: Session, grow_up_id: str) -> Optional[GrowUp]:
        current_grow_up = db.query(GrowUp).get(grow_up_id)
        return current_grow_up

    # @staticmethod
    # def get_grow_up_by_product_farmer_id(db: Session, product_farmer_id: str) -> Optional[GrowUp]:
    #     result = db.query(GrowUp).filter(GrowUp.product_farmer_id == product_farmer_id).all()
    #     return result
#     loi


crud_grow_up = CRUDGrowUp(GrowUp)
