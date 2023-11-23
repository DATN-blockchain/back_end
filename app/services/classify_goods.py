import uuid

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..schemas import ClassifyGoodsCreate, ClassifyGoodsResponse
from ..crud import crud_classify_goods, crud_product


class ClassifyGoodsService:
    def __init__(self, db: Session):
        self.db = db

    async def get_classify_goods_by_id(self, classify_goods_id: str):
        current_classify_goods = crud_classify_goods.get_classify_goods_by_id(db=self.db,
                                                                              classify_goods_id=classify_goods_id)
        if not current_classify_goods:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CART_NOT_FOUND)

        return current_classify_goods

    async def get_classify_goods_by_product_id(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        list_classify_goods = crud_classify_goods.get_classify_goods_by_product_id(db=self.db,
                                                                                   product_id=product_id)
        list_classify_goods = [ClassifyGoodsResponse.from_orm(item) for item in list_classify_goods]
        return list_classify_goods

    @staticmethod
    def permission_data(data: dict, quantity):
        quantity_value = 0
        for k, v in data.items():
            quantity_value += v["quantity"]
        if quantity_value != quantity:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_QUANTITY)
        return quantity

    async def create_classify_goods(self, data: dict, product_id):
        classify_goods = ClassifyGoodsCreate(
            id=str(uuid.uuid4()),
            product_id=product_id,
            data=data
        )
        crud_classify_goods.create(db=self.db, obj_in=classify_goods)
        return data

    async def delete_classify_goods(self, classify_goods_id: str):
        current_classify_goods = crud_classify_goods.get_classify_goods_by_id(db=self.db,
                                                                              classify_goods_id=classify_goods_id)
        if not current_classify_goods:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CART_NOT_FOUND)

        result = crud_classify_goods.remove(db=self.db, entry_id=classify_goods_id)
        return result
