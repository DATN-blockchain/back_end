import uuid

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..model import Product
from ..model.base import ProductStatus
from ..schemas import ProductType, TransactionFMCreate, TransactionFMUpdate, TransactionFMResponse
from ..crud import crud_transaction_fm, crud_product


class TransactionFMService:
    def __init__(self, db: Session):
        self.db = db

    async def get_transaction_fm_by_id(self, transaction_fm_id: str):
        current_transaction_fm = crud_transaction_fm.get_transaction_fm_by_id(db=self.db,
                                                                              transaction_fm_id=transaction_fm_id)
        if not current_transaction_fm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_FM_NOT_FOUND)

        return current_transaction_fm

    async def get_transaction_fm_by_product_id(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        list_transaction_fm = crud_transaction_fm.get_transaction_fm_by_product_id(db=self.db,
                                                                                   product_id=product_id)
        list_transaction_fm = [TransactionFMResponse.from_orm(item) for item in list_transaction_fm]
        return list_transaction_fm

    async def list_transaction_fm(self, product_id: str, user_id, skip: int, limit: int):
        total_transaction_fm, list_transaction_fm = crud_transaction_fm.list_transaction_fm(db=self.db,
                                                                                            user_id=user_id,
                                                                                            product_id=product_id,
                                                                                            skip=skip,
                                                                                            limit=limit)
        list_transaction_fm = [TransactionFMResponse.from_orm(item) for item in list_transaction_fm]
        result = dict(total_transaction_fm=total_transaction_fm, list_transaction_fm=list_transaction_fm)
        return result

    async def create_transaction_fm(self, user_id: str, product_id: str, price: int, quantity: int):

        transaction_fm_create = TransactionFMCreate(
            id=str(uuid.uuid4()),
            user_id=user_id,
            product_id=product_id,
            price=price,
            quantity=quantity)

        result = crud_transaction_fm.create(db=self.db, obj_in=transaction_fm_create)
        return result

    async def has_transaction_fm_permissions(self, user_id: str, transaction_fm_id: str):
        current_transaction_fm = crud_transaction_fm.get_transaction_fm_by_id(db=self.db,
                                                                              transaction_fm_id=transaction_fm_id)
        if not current_transaction_fm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_FM_NOT_FOUND)
        if current_transaction_fm.created_by != user_id:
            raise error_exception_handler(error=Exception(),
                                          app_status=AppStatus.ERROR_TRANSACTION_FM_METHOD_NOT_ALLOWED)
        return current_transaction_fm

    async def update_transaction_fm(self, transaction_fm_id: str, transaction_fm_update: TransactionFMUpdate):
        current_transaction_fm = crud_transaction_fm.get_transaction_fm_by_id(db=self.db,
                                                                              transaction_fm_id=transaction_fm_id)

        result = crud_transaction_fm.update(db=self.db, db_obj=current_transaction_fm, obj_in=transaction_fm_update)
        return result
