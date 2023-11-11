import uuid

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..schemas import CartCreate, CartResponse
from ..crud import crud_cart, crud_product


class CartService:
    def __init__(self, db: Session):
        self.db = db

    async def get_cart_by_id(self, cart_id: str):
        current_cart = crud_cart.get_cart_by_id(db=self.db,
                                                cart_id=cart_id)
        if not current_cart:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_SF_NOT_FOUND)

        return current_cart

    async def get_cart_by_product_id(self, product_id: str):
        current_cart = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_cart:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        list_cart = crud_cart.get_cart_by_product_id(db=self.db,
                                                     product_id=product_id)
        list_cart = [CartResponse.from_orm(item) for item in list_cart]
        return list_cart

    async def list_cart(self, product_id: str, user_id, skip: int, limit: int):
        total_cart, list_cart = crud_cart.list_cart(db=self.db,
                                                    user_id=user_id,
                                                    product_id=product_id,
                                                    skip=skip,
                                                    limit=limit)
        list_cart = [CartResponse.from_orm(item) for item in list_cart]
        result = dict(total_cart=total_cart, list_cart=list_cart)
        return result

    async def create_cart(self, user_id: str, product_id: str, price: int, quantity: int):
        cart_create = CartCreate(
            id=str(uuid.uuid4()),
            user_id=user_id,
            product_id=product_id,
            price=price,
            quantity=quantity)

        result = crud_cart.create(db=self.db, obj_in=cart_create)
        return result

    async def delete_cart(self, cart_id: str):
        current_cart = crud_cart.get_cart_by_id(db=self.db, cart_id=cart_id)
        if not current_cart:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CART_NOT_FOUND)

        result = crud_cart.remove(db=self.db, entry_id=cart_id)
        return result
