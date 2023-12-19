import uuid

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from ..core.settings import settings

from ..model import Product
from ..model.base import ProductStatus, FinancialStatus, TypeTransaction, ConfirmUser
from ..schemas import ProductType, FinancialTransactionCreate, FinancialTransactionUpdate, FinancialTransactionResponse
from ..crud import crud_financial_transaction, crud_product, crud_user
from app.blockchain_web3.actor_provider import ActorProvider


class FinancialTransactionService:
    def __init__(self, db: Session):
        self.db = db

    async def get_financial_transaction_by_id(self, financial_transaction_id: str):
        current_financial_transaction = (crud_financial_transaction.
                                         get_financial_transaction_by_id(db=self.db,
                                                                         financial_transaction_id=financial_transaction_id))
        if not current_financial_transaction:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_FINANCIAL_TRANSACTION_NOT_FOUND)

        return current_financial_transaction

    async def get_financial_transaction_by_transaction_code(self, transaction_code: str):
        current_financial_transaction = (crud_financial_transaction.
                                         get_financial_transaction_by_id(db=self.db,
                                                                         transaction_code=transaction_code))
        if not current_financial_transaction:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_CODE_NOT_FOUND)

        return current_financial_transaction

    async def list_financial_transaction(self, status: FinancialStatus,
                                         type_transaction: TypeTransaction,
                                         skip: int, limit: int, user_id: str = None, ):
        total_financial_transaction, list_financial_transaction = crud_financial_transaction.list_financial_transaction(
            db=self.db,
            status=status,
            type_transaction=type_transaction,
            skip=skip,
            limit=limit,
            user_id=user_id)
        list_financial_transaction = [FinancialTransactionResponse.from_orm(item) for item in
                                      list_financial_transaction]
        result = dict(total_financial_transaction=total_financial_transaction,
                      list_financial_transaction=list_financial_transaction)
        return result

    async def create_financial_transaction(self, user_id: str, type_transaction: TypeTransaction,
                                           transaction_code: str, amount: int):
        current_admin = crud_user.get_admin(db=self.db)
        financial_transaction_create = FinancialTransactionCreate(
            id=str(uuid.uuid4()),
            user_id=user_id,
            type_transaction=type_transaction,
            transaction_code=transaction_code,
            amount=amount)

        actor_provider = ActorProvider()
        tx_hash = actor_provider.deposited(user_id=user_id, amount=amount)
        financial_transaction_create.tx_hash = f'{settings.BLOCK_EXPLORER}{tx_hash}'
        result = crud_financial_transaction.create(db=self.db, obj_in=financial_transaction_create)
        return result, current_admin

    async def update_financial_transaction(self, financial_transaction_id: str,
                                           financial_transaction_update: ConfirmUser):
        current_financial_transaction = (crud_financial_transaction.
                                         get_financial_transaction_by_id(db=self.db,
                                                                         financial_transaction_id=financial_transaction_id))
        if current_financial_transaction.status not in FinancialStatus.PENDING:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_ACTION)

        if not current_financial_transaction:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_CODE_NOT_FOUND)

        current_user = crud_user.get_user_by_id(db=self.db, user_id=current_financial_transaction.user_id)
        if current_financial_transaction.type_transaction == TypeTransaction.DEPOSIT:
            if financial_transaction_update == ConfirmUser.ACCEPT:
                amount = current_financial_transaction.amount / 1000
                account_balance = current_user.account_balance + amount
                status = FinancialStatus.DONE
                update_account_balance = dict(account_balance=account_balance)

                actor_provider = ActorProvider()
                tx_hash = actor_provider.deposited(user_id=current_user.id, amount=amount)
                update_account_balance["tx_hash"] = f'{settings.BLOCK_EXPLORER}{tx_hash}'
                crud_user.update(db=self.db, db_obj=current_user, obj_in=update_account_balance)
            else:
                status = FinancialStatus.FAIL

            crud_financial_transaction.update_status_financial_transaction(db=self.db,
                                                                           db_obj=current_financial_transaction,
                                                                           status=status)

        else:
            pass
        # breakpoint()
        return AppStatus.SUCCESS
