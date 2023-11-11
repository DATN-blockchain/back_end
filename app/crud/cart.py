from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import CRUDBase
from ..model import Cart

from ..schemas import CartCreate, CartUpdate


class CRUDCart(CRUDBase[Cart, CartCreate, CartUpdate]):
    @staticmethod
    def get_cart_by_product_id(db: Session, product_id: str):
        current_cart = db.query(Cart).filter(Cart.product_id == product_id).all()
        return current_cart

    @staticmethod
    def get_cart_by_id(db: Session, cart_id: str) -> Optional[Cart]:
        current_cart = db.query(Cart).get(cart_id)
        return current_cart

    @staticmethod
    def list_cart(db: Session, skip: int, limit: int, user_id: str, product_id: str = None):
        db_query = db.query(Cart).filter(Cart.user_id == user_id)
        if product_id is not None:
            db_query = db_query.filter(Cart.product_id == product_id)

        total_cart = db_query.count()
        list_cart = db_query.order_by(desc(Cart.created_at)).offset(skip).limit(limit).all()
        return total_cart, list_cart


crud_cart = CRUDCart(Cart)
