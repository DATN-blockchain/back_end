import logging
import uuid

from typing import Dict, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from .base import CRUDBase
from ..model import ProductFarmer, Product
from ..model.base import ProductType, ProductStatus

from ..schemas import ProductFarmerCreate, ProductFarmerUpdate

logger = logging.getLogger(__name__)


class CRUDProductFarmer(CRUDBase[ProductFarmer, ProductFarmerCreate, ProductFarmerUpdate]):
    @staticmethod
    def get_product_farmer_by_id(db: Session, product_farmer_id: str) -> Optional[ProductFarmer]:
        current_product_farmer = db.query(ProductFarmer).get(product_farmer_id)
        return current_product_farmer


crud_product_farmer = CRUDProductFarmer(ProductFarmer)
