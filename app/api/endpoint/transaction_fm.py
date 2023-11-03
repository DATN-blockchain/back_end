from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.model.base import ProductStatus, ProductType
from app.utils.response import make_response_object

from app.schemas.transaction_fm import TransactionFMUpdate
from app.model import User
from app.services import TransactionFMService

router = APIRouter()


@router.get("/transaction_fm/{product_id}/get")
async def get_transaction_fm_by_product_id(
        product_id: str,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)):
    transaction_fm_service = TransactionFMService(db=db)

    transaction_fm_response = await transaction_fm_service.get_transaction_fm_by_product_id(product_id=product_id)
    return make_response_object(transaction_fm_response)


@router.get("/transaction_fm/list")
async def list_transaction_fm(
        product_id: str = None,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
        skip=0,
        limit=10):
    transaction_fm_service = TransactionFMService(db=db)

    transaction_fm_response = await transaction_fm_service.list_transaction_fm(product_id=product_id,
                                                                               user_id=user.id,
                                                                               skip=skip, limit=limit)
    return make_response_object(transaction_fm_response)


@router.get("/transaction_fm/{transaction_fm_id}")
async def get_transaction_fm_by_id(transaction_fm_id: str,
                                   user: User = Depends(oauth2.get_current_user),
                                   db: Session = Depends(get_db)):
    transaction_fm_service = TransactionFMService(db=db)

    transaction_fm_response = await transaction_fm_service.get_transaction_fm_by_id(transaction_fm_id=transaction_fm_id)
    return make_response_object(transaction_fm_response)


@router.put("/transaction_fm/update/{transaction_fm_id}")
async def update_transaction_fm(transaction_fm_id: str,
                                transaction_fm_update: TransactionFMUpdate,
                                user: User = Depends(oauth2.get_current_user),
                                db: Session = Depends(get_db)):
    transaction_fm_service = TransactionFMService(db=db)

    # authorization
    await transaction_fm_service.has_transaction_fm_permissions(user_id=user.id, transaction_fm_id=transaction_fm_id)

    trans_fm_response = await transaction_fm_service.update_transaction_fm(transaction_fm_id=transaction_fm_id,
                                                                           transaction_fm_update=transaction_fm_update)

    return make_response_object(trans_fm_response)
