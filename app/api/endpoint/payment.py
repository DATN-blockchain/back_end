import logging
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.api.depend import oauth2
from app.db.database import get_db
from app.model import User
from app.model.base import BankCode, LanguageEnum
from app.services import UserService

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
async def payments_return(request: Request, db: Session = Depends(get_db)):
    service = UserService(db=db)
    result = await service.payment_return_in_user(request=request)
    return result
