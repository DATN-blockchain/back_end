import uuid

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from ..model import User
from ..model.base import UserSystemRole, ProductType

from ..schemas import CartCreate, CartResponse, CartCreateParam
from ..crud import crud_cart, crud_product


class CartService:
    def __init__(self, db: Session):
        self.db = db

    async def get_cart_by_id(self, cart_id: str):
        current_cart = crud_cart.get_cart_by_id(db=self.db,
                                                cart_id=cart_id)
        if not current_cart:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CART_NOT_FOUND)

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

    async def create_cart(self, user: User, cart_create: CartCreateParam):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=cart_create.product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        if user.system_role == UserSystemRole.SEEDLING_COMPANY:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_YOU_CANNOT_ADD_TO_CART)
        elif user.system_role == UserSystemRole.FARMER:
            if current_product.product_type != ProductType.SEEDLING_COMPANY:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_PERMISSION_TO_CHOOSE_THE_SEEDLING_COMPANY)
        elif user.system_role == UserSystemRole.MANUFACTURER:
            if current_product.product_type != ProductType.FARMER:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_PERMISSION_TO_CHOOSE_FARMER)
        current_cart = crud_cart.get_cart_by_product_id(db=self.db, product_id=current_product.id, user_id=user.id)

        if current_cart:
            new_quantity = current_cart.quantity + cart_create.quantity
            new_price = current_product.price * new_quantity
            obj_in = dict(quantity=new_quantity, price=new_price)
            result = crud_cart.update(db=self.db, db_obj=current_cart, obj_in=obj_in)
        else:
            cart_create = CartCreate(
                id=str(uuid.uuid4()),
                user_id=user.id,
                product_id=cart_create.product_id,
                price=cart_create.price,
                quantity=cart_create.quantity)
            result = crud_cart.create(db=self.db, obj_in=cart_create)
        return result

    async def delete_cart(self, cart_id: str):
        current_cart = crud_cart.get_cart_by_id(db=self.db, cart_id=cart_id)
        if not current_cart:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CART_NOT_FOUND)

        result = crud_cart.remove(db=self.db, entry_id=cart_id)
        return result
