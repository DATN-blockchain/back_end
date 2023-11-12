import logging
from datetime import datetime, timedelta

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, extract
from .base import CRUDBase
from ..model import Product, TransactionSF, ProductFarmer, ProductManufacturer, TransactionFM
from ..model.base import ProductStatus, ProductType

from ..schemas import ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)


class ProductWithTotalQuantity:
    def __init__(self, product, total_quantity):
        self.product = product
        self.total_quantity = total_quantity


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    @staticmethod
    def get_product_by_id(db: Session, product_id: str) -> Product:
        current_product = db.query(Product).filter(Product.id == product_id).first()
        return current_product

    @staticmethod
    def get_statistical_product(db: Session):
        db_query = db.query(Product)
        seedling_count = db_query.filter(Product.product_type == ProductType.SEEDLING_COMPANY).count()
        farmer_count = db_query.filter(Product.product_type == ProductType.FARMER).count()
        manufacturer_count = db_query.filter(Product.product_type == ProductType.MANUFACTURER).count()
        total_product = db_query.count()
        result = dict(total_product=total_product,
                      seedling_count=seedling_count, farmer_count=farmer_count,
                      manufacturer_count=manufacturer_count)
        return result

    @staticmethod
    def get_statistical_product_me(db: Session, user_id: str):
        db_query = db.query(Product).filter(Product.created_by == user_id)
        total_sales = db.query(func.sum(Product.number_of_sales)).filter(Product.created_by == user_id).scalar()
        total_product = db_query.count()
        result = dict(total_product=total_product, total_sales=total_sales)
        return result

    @staticmethod
    def get_product_by_me(db: Session, user_id: str, name: str = None,
                          skip: int = None, limit: int = None):
        db_query = db.query(Product).filter(Product.created_by == user_id)
        if name is not None:
            db_query = db_query.filter(Product.name.ilike(f'%{name}%'))
        total_product = db_query.count()
        if skip and limit is not None:
            list_product = db_query.order_by(desc(Product.created_at)).offset(skip).limit(limit).all()
        else:
            list_product = db_query.order_by(desc(Product.created_at)).all()
        return total_product, list_product

    @staticmethod
    def get_product_top_selling(db: Session, product_type: ProductType):
        current_date = datetime.now()
        start_date = current_date - timedelta(days=7)
        if product_type == ProductType.SEEDLING_COMPANY:
            top_selling = db.query(Product, func.sum(TransactionSF.quantity).label('total_quantity'),
                                   func.count(TransactionSF.quantity).label('total_sales')).join(
                TransactionSF, TransactionSF.product_id == Product.id).filter(
                TransactionSF.created_at >= start_date,
                TransactionSF.created_at <= current_date).group_by(Product).order_by(
                func.sum(TransactionSF.quantity).desc()).limit(10).all()
        elif product_type == ProductType.FARMER:
            top_selling = db.query(Product, func.sum(TransactionFM.quantity).label('total_quantity'),
                                   func.count(TransactionFM.quantity).label('total_sales')).join(
                TransactionFM, TransactionFM.product_id == Product.id).filter(
                TransactionFM.created_at >= start_date,
                TransactionFM.created_at <= current_date).group_by(Product).order_by(
                func.sum(TransactionFM.quantity).desc()).limit(10).all()
        else:
            return []

        return top_selling

    @staticmethod
    def get_transaction_sf_in_product(db: Session, user_id: str, transaction_id: str):
        db_query = (db.query(Product).join(ProductFarmer, ProductFarmer.product_id == Product.id).filter(
            Product.created_by == user_id)).filter(ProductFarmer.transaction_sf_id == transaction_id).first()
        return db_query

    @staticmethod
    def get_transaction_fm_in_product(db: Session, user_id: str, transaction_id: str):
        db_query = (db.query(Product).join(ProductManufacturer, ProductManufacturer.product_id == Product.id).filter(
            Product.created_by == user_id)).filter(ProductManufacturer.transaction_fm_id == transaction_id).first()
        return db_query

    @staticmethod
    def list_product(db: Session, skip: int, limit: int, name: str = None, user_id: str = None):
        db_query = db.query(Product).filter(Product.product_status == ProductStatus.PUBLISH)
        if name is not None:
            db_query = db_query.filter(Product.name.ilike(f'%{name}%'))
        if user_id is not None:
            db_query = db_query.filter(Product.created_by == user_id)
        total_product = db_query.count()
        list_product = db_query.order_by(desc(Product.created_at)).offset(skip).limit(limit).all()
        return total_product, list_product

    @staticmethod
    def update_product_status(db: Session, current_product: Product, product_status: ProductStatus):
        current_product.product_status = product_status
        db.commit()
        db.refresh(current_product)
        return current_product

    @staticmethod
    def update_is_sale(db: Session, current_product: Product, is_sale: bool):
        current_product.is_sale = is_sale
        db.commit()
        db.refresh(current_product)
        return current_product

    @staticmethod
    def get_chart_product(db: Session, product_id: int):
        current_month = datetime.now().month
        current_year = datetime.now().year
        current_product = db.query(Product).filter(Product.id == product_id).first()
        product_chart = {}
        for i in range(6):
            month = current_month - i
            year = current_year
            if month <= 0:
                month += 12
                year -= 1

            if current_product.product_type == ProductType.SEEDLING_COMPANY:
                item = TransactionSF
            elif current_product.product_type == ProductType.FARMER:
                item = TransactionFM
            else:
                return product_chart
            count_number_of_sale = db.query(Product, item.created_at).join(item, Product.id == item.product_id).filter(
                Product.id == product_id, extract('year', item.created_at) == year,
                extract('month', item.created_at) == month).count()
            total_quantity = db.query(func.coalesce(func.sum(TransactionSF.quantity), 0)) \
                .join(Product, Product.id == item.product_id) \
                .filter(Product.id == product_id, extract('year', item.created_at) == year,
                        extract('month', item.created_at) == month) \
                .scalar()

            product_chart[str(month)] = {
                "count_number_of_sale": count_number_of_sale,
                "total_quantity": total_quantity,
            }

        return product_chart


crud_product = CRUDProduct(Product)
