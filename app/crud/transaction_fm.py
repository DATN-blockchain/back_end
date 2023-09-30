import logging

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import CRUDBase
from ..model import TransactionFM

from ..schemas import TransactionFMCreate, TransactionFMUpdate

logger = logging.getLogger(__name__)


class CRUDTransactionFM(CRUDBase[TransactionFM, TransactionFMCreate, TransactionFMUpdate]):
    @staticmethod
    def get_transaction_fm_by_id(db: Session, transaction_fm_id: str) -> Optional[TransactionFM]:
        current_transaction_fm = db.query(TransactionFM).get(transaction_fm_id)
        return current_transaction_fm

    @staticmethod
    def list_transaction_fm(db: Session, skip: int, limit: int, user_id: str, product_id: str = None):
        db_query = db.query(TransactionFM).filter(TransactionFM.user_id == user_id)
        if product_id is not None:
            db_query = db_query.filter(TransactionFM.product_id == product_id)

        total_transaction_fm = db_query.count()
        list_transaction_fm = db_query.order_by(desc(TransactionFM.created_at)).offset(skip).limit(limit).all()
        return total_transaction_fm, list_transaction_fm


crud_transaction_fm = CRUDTransactionFM(TransactionFM)
