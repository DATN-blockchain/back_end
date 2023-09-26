import uuid

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..model import Product
from ..model.base import ProductStatus
from ..schemas import ProductType, TransactionSFCreate, TransactionSFUpdate, TransactionSFResponse
from ..crud import crud_transaction_sf, crud_product


class TransactionSFService:
    def __init__(self, db: Session):
        self.db = db

    async def get_transaction_sf_by_id(self, transaction_sf_id: str):
        current_transaction_sf = crud_transaction_sf.get_transaction_sf_by_id(db=self.db,
                                                                              transaction_sf_id=transaction_sf_id)
        if not current_transaction_sf:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_SF_NOT_FOUND)

        return current_transaction_sf

    async def list_transaction_sf(self, product_id: str, user_id, skip: int, limit: int):
        total_transaction_sf, list_transaction_sf = crud_transaction_sf.list_transaction_sf(db=self.db,
                                                                                            user_id=user_id,
                                                                                            product_id=product_id,
                                                                                            skip=skip,
                                                                                            limit=limit)
        list_transaction_sf = [TransactionSFResponse.from_orm(item) for item in list_transaction_sf]
        result = dict(total_transaction_sf=total_transaction_sf, list_transaction_sf=list_transaction_sf)
        return result

    async def create_transaction_sf(self, user_id: str, product_id: str, price: int, quantity: int):

        transaction_sf_create = TransactionSFCreate(
            id=str(uuid.uuid4()),
            user_id=user_id,
            product_id=product_id,
            price=price,
            quantity=quantity)

        result = crud_transaction_sf.create(db=self.db, obj_in=transaction_sf_create)
        return result

    async def has_transaction_sf_permissions(self, user_id: str, transaction_sf_id: str):
        current_transaction_sf = crud_transaction_sf.get_transaction_sf_by_id(db=self.db,
                                                                              transaction_sf_id=transaction_sf_id)
        if not current_transaction_sf:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_SF_NOT_FOUND)
        if current_transaction_sf.created_by != user_id:
            raise error_exception_handler(error=Exception(),
                                          app_status=AppStatus.ERROR_TRANSACTION_SF_METHOD_NOT_ALLOWED)
        return current_transaction_sf

    async def update_transaction_sf(self, transaction_sf_id: str, transaction_sf_update: TransactionSFUpdate):
        current_transaction_sf = crud_transaction_sf.get_transaction_sf_by_id(db=self.db,
                                                                              transaction_sf_id=transaction_sf_id)

        result = crud_transaction_sf.update(db=self.db, db_obj=current_transaction_sf, obj_in=transaction_sf_update)
        return result
