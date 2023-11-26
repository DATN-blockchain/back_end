from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from app.db.database import get_db
from app.api.depend import oauth2
from app.model.base import FinancialStatus, TypeTransaction, ConfirmUser
from app.utils.response import make_response_object

from app.model.base import NotificationType
from app.utils.background_tasks import send_notification
from app.model import User
from app.services import FinancialTransactionService, NotificationService
from app.constant.template import FinancialTransactionTemplate

router = APIRouter()


@router.get("/financial_transaction/list")
async def list_financial_transaction(
        status: FinancialStatus = None,
        type_transaction: TypeTransaction = None,
        transaction_code: str = None,
        user: User = Depends(oauth2.admin),
        db: Session = Depends(get_db),
        skip=0,
        limit=10):
    financial_transaction_service = FinancialTransactionService(db=db)

    financial_transaction_response = await financial_transaction_service.list_financial_transaction(
        transaction_code=transaction_code,
        status=status,
        type_transaction=type_transaction,
        skip=skip, limit=limit)
    return make_response_object(financial_transaction_response)


@router.get("/financial_transaction/{financial_transaction_id}")
async def get_financial_transaction_by_id(financial_transaction_id: str,
                                          user: User = Depends(oauth2.admin),
                                          db: Session = Depends(get_db)):
    financial_transaction_service = FinancialTransactionService(db=db)

    financial_transaction_response = await financial_transaction_service.get_financial_transaction_by_id(
        financial_transaction_id=financial_transaction_id)
    return make_response_object(financial_transaction_response)


@router.post("/financial_transaction/create")
async def create_financial_transaction(type_transaction: TypeTransaction,
                                       transaction_code: str,
                                       amount: int,
                                       background_tasks: BackgroundTasks,
                                       user: User = Depends(oauth2.get_current_user),
                                       db: Session = Depends(get_db)):
    financial_transaction_service = FinancialTransactionService(db=db)
    notification_service = NotificationService(db=db)

    financial_response, current_admin = await (financial_transaction_service.
                                               create_financial_transaction(user_id=user.id,
                                                                            type_transaction=type_transaction,
                                                                            transaction_code=transaction_code,
                                                                            amount=amount))
    if type_transaction == TypeTransaction.DEPOSIT:
        action = "deposit"
        message_template = FinancialTransactionTemplate.Deposit_MSG
    else:
        action = "withdraw"
        message_template = FinancialTransactionTemplate.Withdraw_MSG

    background_tasks.add_task(
        send_notification, notification_service, entity=financial_response,
        notification_type=NotificationType.TRANSACTION_NOTIFICATION,
        message_template=message_template, action=action, current_user=user, owner=current_admin, price=amount
    )

    return make_response_object(financial_response)


@router.put("/financial_transaction/update/{financial_transaction_id}")
async def update_financial_transaction(financial_transaction_id: str,
                                       financial_transaction_update: ConfirmUser,
                                       user: User = Depends(oauth2.admin),
                                       db: Session = Depends(get_db)):
    financial_transaction_service = FinancialTransactionService(db=db)

    financial_transaction_response = await financial_transaction_service.update_financial_transaction(
        financial_transaction_id=financial_transaction_id,
        financial_transaction_update=financial_transaction_update)

    return make_response_object(financial_transaction_response)
