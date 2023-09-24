import uuid

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..model import Product
from ..model.base import ProductStatus
from ..schemas import ProductType, MarketplaceCreate, MarketplaceUpdate, MarketplaceResponse
from ..crud import crud_marketplace, crud_product


class MarketplaceService:
    def __init__(self, db: Session):
        self.db = db

    async def get_marketplace_by_id(self, marketplace_id: str):
        current_marketplace = crud_marketplace.get_marketplace_by_id(db=self.db, marketplace_id=marketplace_id)
        if not current_marketplace:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        return current_marketplace

    async def list_marketplace(self, product_id: str, order_type: ProductType, skip: int, limit: int):
        total_marketplace, list_marketplace = crud_marketplace.list_marketplace(db=self.db, product_id=product_id,
                                                                                order_type=order_type, skip=skip,
                                                                                limit=limit)
        list_marketplace = [MarketplaceResponse.from_orm(item) for item in list_marketplace]
        result = dict(total_marketplace=total_marketplace, list_marketplace=list_marketplace)
        return result

    async def create_marketplace(self, user_id: str, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)

        if current_product.created_by != user_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)

        marketplace_create = MarketplaceCreate(
            id=str(uuid.uuid4()),
            order_type=current_product.product_type,
            order_id=current_product.id,
            order_by=user_id)

        result = crud_marketplace.create(db=self.db, obj_in=marketplace_create)
        return result

    async def has_marketplace_permissions(self, user_id: str, marketplace_id: str):
        current_marketplace = crud_marketplace.get_marketplace_by_id(db=self.db, marketplace_id=marketplace_id)
        if not current_marketplace:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        if current_marketplace.created_by != user_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)
        return current_marketplace

    async def update_marketplace(self, marketplace_id: str, marketplace_update: MarketplaceUpdate):
        current_marketplace = crud_marketplace.get_marketplace_by_id(db=self.db, marketplace_id=marketplace_id)

        result = crud_marketplace.update(db=self.db, db_obj=current_marketplace, obj_in=marketplace_update)
        return result

    # async def delete_marketplace(self, marketplace_id: str):
    #     current_marketplace = crud_marketplace.get_marketplace_by_id(db=self.db, marketplace_id=marketplace_id)
    #     if not current_marketplace:
    #         raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
    #
    #     result = crud_marketplace.remove(db=self.db, entry_id=marketplace_id)
    #     return result