from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import CRUDBase
from ..model import TransactionFM
from ..model.base import ConfirmStatusProduct

from ..schemas import TransactionFMCreate, TransactionFMUpdate


class CRUDTransactionFM(CRUDBase[TransactionFM, TransactionFMCreate, TransactionFMUpdate]):
    @staticmethod
    def get_transaction_fm_by_product_id(db: Session, product_id: str):
        current_transaction_fm = db.query(TransactionFM).filter(TransactionFM.product_id == product_id).all()
        return current_transaction_fm

    @staticmethod
    def get_statistical_transaction_fm(db: Session):
        db_query = db.query(TransactionFM)
        result = dict(total_transaction_fm=db_query.count())
        return result

    @staticmethod
    def get_transaction_fm_by_id(db: Session, transaction_fm_id: str) -> Optional[TransactionFM]:
        current_transaction_fm = db.query(TransactionFM).get(transaction_fm_id)
        return current_transaction_fm

    @staticmethod
    def get_product_order_by_user(db: Session, user_id: str, skip: int, limit: int,
                                  status: ConfirmStatusProduct = None):
        db_query = db.query(TransactionFM).filter(TransactionFM.order_by == user_id)
        if status:
            db_query = db_query.filter(TransactionFM.status == status)
        total_transaction = db_query.count()
        list_transaction = db_query.order_by(desc(TransactionFM.created_at)).offset(skip).limit(limit).all()
        return total_transaction, list_transaction

    @staticmethod
    def get_history_sale(db: Session, user_id: str, skip: int, limit: int):
        db_query = db.query(TransactionFM).filter(TransactionFM.order_by == user_id)
        total_transaction = db_query.count()
        list_transaction = db_query.order_by(desc(TransactionFM.created_at)).offset(skip).limit(limit).all()
        return total_transaction, list_transaction

    @staticmethod
    def list_transaction_fm(db: Session, skip: int, limit: int, user_id: str, product_id: str = None):
        db_query = db.query(TransactionFM).filter(TransactionFM.user_id == user_id)
        if product_id:
            db_query = db_query.filter(TransactionFM.product_id == product_id)

        total_transaction_fm = db_query.count()
        list_transaction_fm = db_query.order_by(desc(TransactionFM.created_at)).offset(skip).limit(limit).all()
        return total_transaction_fm, list_transaction_fm

    @staticmethod
    def update_confirm_order(db: Session, current_transaction: TransactionFM, status: ConfirmStatusProduct):
        current_transaction.status = status
        db.commit()
        db.refresh(current_transaction)
        return current_transaction


crud_transaction_fm = CRUDTransactionFM(TransactionFM)
