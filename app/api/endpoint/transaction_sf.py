from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.model.base import ProductStatus, ProductType
from app.utils.response import make_response_object

from app.schemas.transaction_sf import TransactionSFUpdate
from app.model import User
from app.services import TransactionSFService

router = APIRouter()


@router.get("/transaction_sf/list")
async def list_transaction_sf(
        product_id: str = None,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
        skip=0,
        limit=10):
    transaction_sf_service = TransactionSFService(db=db)

    transaction_sf_response = await transaction_sf_service.list_transaction_sf(product_id=product_id,
                                                                               skip=skip, limit=limit)
    return make_response_object(transaction_sf_response)


@router.get("/transaction_sf/{transaction_sf_id}")
async def get_transaction_sf_by_id(transaction_sf_id: str,
                                   user: User = Depends(oauth2.get_current_user),
                                   db: Session = Depends(get_db)):
    transaction_sf_service = TransactionSFService(db=db)

    transaction_sf_response = await transaction_sf_service.get_transaction_sf_by_id(transaction_sf_id=transaction_sf_id)
    return make_response_object(transaction_sf_response)


@router.put("/transaction_sf/update/{transaction_sf_id}")
async def update_transaction_sf(transaction_sf_id: str,
                                transaction_sf_update: TransactionSFUpdate,
                                user: User = Depends(oauth2.get_current_user),
                                db: Session = Depends(get_db)):
    transaction_sf_service = TransactionSFService(db=db)

    # authorization
    await transaction_sf_service.has_transaction_sf_permissions(user_id=user.id, transaction_sf_id=transaction_sf_id)

    trans_sf_response = await transaction_sf_service.update_transaction_sf(transaction_sf_id=transaction_sf_id,
                                                                           transaction_sf_update=transaction_sf_update)

    return make_response_object(trans_sf_response)
