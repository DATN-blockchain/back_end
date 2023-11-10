import logging
import uuid

from typing import Dict, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from .base import CRUDBase
from ..model import Marketplace, Product
from ..model.base import ProductType, ProductStatus

from ..schemas import MarketplaceCreate, MarketplaceUpdate

logger = logging.getLogger(__name__)


class CRUDMarketplace(CRUDBase[Marketplace, MarketplaceCreate, MarketplaceUpdate]):
    @staticmethod
    def get_marketplace_by_id(db: Session, marketplace_id: str) -> Optional[Marketplace]:
        current_marketplace = db.query(Marketplace).get(marketplace_id)
        return current_marketplace

    @staticmethod
    def get_marketplace_by_product_id(db: Session, product_id: str) -> Optional[Marketplace]:
        current_marketplace = db.query(Marketplace).filter(Marketplace.order_id == product_id).first()
        return current_marketplace

    @staticmethod
    def list_marketplace(db: Session, skip: int, limit: int, order_type: ProductType = None,
                         product_id: str = None, name_product: str = None):
        db_query = db.query(Marketplace).join(Product, Marketplace.order_id == Product.id).filter(
            Product.product_status == ProductStatus.PUBLISH)
        if order_type is not None:
            db_query = db_query.filter(Marketplace.order_type == order_type)
        if product_id is not None:
            db_query = db_query.filter(Marketplace.order_id == product_id)
        if name_product is not None:
            db_query = db_query.filter(Product.name.ilike(f'%{name_product}%'))

        total_marketplace = db_query.count()
        list_marketplace = db_query.order_by(desc(Marketplace.created_at)).offset(skip).limit(limit).all()
        return total_marketplace, list_marketplace


crud_marketplace = CRUDMarketplace(Marketplace)
