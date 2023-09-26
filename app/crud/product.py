import logging
import uuid

from typing import Dict, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from .base import CRUDBase
from ..model import Product, TransactionSF, ProductFarmer
from ..model.base import ProductStatus

from ..schemas import ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    @staticmethod
    def get_product_by_id(db: Session, product_id: str) -> Optional[Product]:
        current_product = db.query(Product).get(product_id)
        return current_product

    @staticmethod
    def get_product_by_me(db: Session, user_id: str, skip: int = None, limit: int = None):
        db_query = db.query(Product).filter(Product.created_by == user_id)
        total_product = db_query.count()
        if skip and limit is not None:
            list_product = db_query.offset(skip).limit(limit).all()
        else:
            list_product = db_query.all()
        return total_product, list_product

    @staticmethod
    def get_transaction_in_product(db: Session, user_id: str, transaction_id: str):
        db_query = (db.query(Product).join(ProductFarmer, ProductFarmer.product_id == Product.id).filter(
            Product.created_by == user_id)).filter(ProductFarmer.transaction_sf_id == transaction_id).first()
        return db_query

    @staticmethod
    def list_product(db: Session, skip: int, limit: int):
        db_query = db.query(Product).filter(Product.product_status == ProductStatus.PUBLISH)
        total_product = db_query.count()
        list_product = db_query.order_by(desc(Product.created_at)).offset(skip).limit(limit).all()
        return total_product, list_product

    @staticmethod
    def update_product_status(db: Session, current_product: Product, product_status: ProductStatus):
        current_product.product_status = product_status
        db.commit()
        db.refresh(current_product)
        return current_product


crud_product = CRUDProduct(Product)
