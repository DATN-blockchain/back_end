import logging
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from app.api.depend import oauth2
from app.constant.template import FinancialTransactionTemplate
from app.db.database import get_db
from app.model import User
from app.model.base import BankCode, LanguageEnum, NotificationType
from app.services import UserService, NotificationService
from app.utils.background_tasks import send_notification

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post('/payment')
async def payments(request: Request, amount: int, bank_code: BankCode, language: LanguageEnum = LanguageEnum.VIETNAMESE,
                   user: User = Depends(oauth2.get_current_user),
                   db: Session = Depends(get_db)):
    service = UserService(db=db)
    result = await service.payment(request=request, amount=amount, bank_code=bank_code, language=language,
                                   user_id=user.id)
    return result


@router.get("/payment/payments_return")
async def payments_return(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    service = UserService(db=db)
    notification_service = NotificationService(db=db)
    financial_response, current_user, current_admin, amount = await service.payment_return_in_user(request=request)
    message_template = FinancialTransactionTemplate.Deposit_MSG
    background_tasks.add_task(
        send_notification, notification_service, entity=financial_response,
        notification_type=NotificationType.TRANSACTION_NOTIFICATION,
        message_template=message_template, action="deposit",
        current_user=current_user, owner=current_admin, price=amount
    )
    return RedirectResponse(url='https://www.facebook.com/')
