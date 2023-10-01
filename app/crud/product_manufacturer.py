import logging
import uuid

from typing import Dict, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from .base import CRUDBase
from ..model import ProductManufacturer, Product
from ..model.base import ProductType, ProductStatus

from ..schemas import ProductManufacturerCreate, ProductManufacturerUpdate

logger = logging.getLogger(__name__)


class CRUDProductManufacturer(CRUDBase[ProductManufacturer, ProductManufacturerCreate, ProductManufacturerUpdate]):
    @staticmethod
    def get_product_manufacturer_by_id(db: Session, product_manufacturer_id: str) -> Optional[ProductManufacturer]:
        current_product_manufacturer = db.query(ProductManufacturer).get(product_manufacturer_id)
        return current_product_manufacturer

    @staticmethod
    def get_product_manufacturer_by_product_id(db: Session, product_id: str) -> Optional[ProductManufacturer]:
        current_product_manufacturer = db.query(ProductManufacturer).filter(
            ProductManufacturer.product_id == product_id).first()
        return current_product_manufacturer


crud_product_manufacturer = CRUDProductManufacturer(ProductManufacturer)
