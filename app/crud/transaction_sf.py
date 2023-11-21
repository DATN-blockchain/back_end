import logging

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import CRUDBase
from ..model import TransactionSF, Product
from ..model.base import ProductType, ProductStatus, ConfirmStatusProduct

from ..schemas import TransactionSFCreate, TransactionSFUpdate

logger = logging.getLogger(__name__)


class CRUDTransactionSF(CRUDBase[TransactionSF, TransactionSFCreate, TransactionSFUpdate]):

    @staticmethod
    def get_transaction_sf_by_product_id(db: Session, product_id: str):
        current_transaction_sf = db.query(TransactionSF).filter(TransactionSF.product_id == product_id).all()
        return current_transaction_sf

    @staticmethod
    def get_statistical_transaction_sf(db: Session):
        db_query = db.query(TransactionSF).count()
        result = dict(total_transaction_sf=db_query)
        return result

    @staticmethod
    def get_transaction_sf_by_id(db: Session, transaction_sf_id: str) -> Optional[TransactionSF]:
        current_transaction_sf = db.query(TransactionSF).get(transaction_sf_id)
        return current_transaction_sf

    @staticmethod
    def get_product_order_by_user(db: Session, user_id: str, skip: int, limit: int,
                                  status: ConfirmStatusProduct = None):
        db_query = db.query(TransactionSF).filter(TransactionSF.order_by == user_id)
        if status:
            db_query = db_query.filter(TransactionSF.status == status)
        total_transaction = db_query.count()
        list_transaction = db_query.order_by(desc(TransactionSF.created_at)).offset(skip).limit(limit).all()
        return total_transaction, list_transaction

    @staticmethod
    def list_transaction_sf(db: Session, skip: int, limit: int, user_id: str, product_id: str = None):
        db_query = db.query(TransactionSF).filter(TransactionSF.user_id == user_id)
        if product_id is not None:
            db_query = db_query.filter(TransactionSF.product_id == product_id)

        total_transaction_sf = db_query.count()
        list_transaction_sf = db_query.order_by(desc(TransactionSF.created_at)).offset(skip).limit(limit).all()
        return total_transaction_sf, list_transaction_sf


crud_transaction_sf = CRUDTransactionSF(TransactionSF)
