import logging

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import CRUDBase
from ..model import FinancialTransaction
from ..model.base import FinancialStatus

from ..schemas import FinancialTransactionCreate, FinancialTransactionUpdate

logger = logging.getLogger(__name__)


class CRUDFinancialTransaction(CRUDBase[FinancialTransaction, FinancialTransactionCreate, FinancialTransactionUpdate]):
    @staticmethod
    def get_financial_transaction_by_id(db: Session, financial_transaction_id: str) -> Optional[FinancialTransaction]:
        current_financial_transaction = db.query(FinancialTransaction).get(financial_transaction_id)
        return current_financial_transaction

    @staticmethod
    def get_financial_transaction_by_transaction_code(db: Session, transaction_code: str):
        result = db.query(FinancialTransaction).filter(
            FinancialTransaction.transaction_code == transaction_code).first()
        return result

    @staticmethod
    def list_financial_transaction(db: Session, skip: int, limit: int, transaction_code: str = None,
                                   status: str = None, type_transaction: str = None):
        db_query = db.query(FinancialTransaction)
        if transaction_code is not None:
            db_query = db_query.filter(FinancialTransaction.transaction_code == transaction_code)
        if status is not None:
            db_query = db_query.filter(FinancialTransaction.status == status)
        if type_transaction is not None:
            db_query = db_query.filter(FinancialTransaction.type_transaction == type_transaction)

        total_financial_transaction = db_query.count()
        list_financial_transaction = db_query.order_by(desc(FinancialTransaction.created_at)).offset(skip).limit(
            limit).all()
        return total_financial_transaction, list_financial_transaction

    @staticmethod
    def update_status_financial_transaction(db: Session, db_obj: FinancialTransaction, status: FinancialStatus):
        db_obj.status = status
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_financial_transaction = CRUDFinancialTransaction(FinancialTransaction)
