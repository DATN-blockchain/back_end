from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.schemas import CartCreateParam
from app.utils.response import make_response_object

from app.schemas.cart import CartUpdate
from app.model import User
from app.services import CartService

router = APIRouter()


@router.get("/cart/{cart_id}/get")
async def get_cart_by_id(cart_id: str,
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    cart_service = CartService(db=db)

    cart_response = await cart_service.get_cart_by_id(cart_id=cart_id)
    return make_response_object(cart_response)


@router.get("/cart/list")
async def list_cart(
        product_id: str = None,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
        skip=0,
        limit=10):
    cart_service = CartService(db=db)

    cart_response = await cart_service.list_cart(product_id=product_id,
                                                 user_id=user.id,
                                                 skip=skip, limit=limit)
    return make_response_object(cart_response)


@router.post("/cart/create")
async def create_cart(cart_create: CartCreateParam,
                      user: User = Depends(oauth2.get_current_user),
                      db: Session = Depends(get_db)):
    cart_service = CartService(db=db)
    product_response = await cart_service.create_cart(user=user, cart_create=cart_create)
    return make_response_object(product_response)


@router.delete("/cart/{cart_id}/delete")
async def delete_product(cart_id: str,
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    cart_service = CartService(db=db)

    product_response = await cart_service.delete_cart(cart_id=cart_id)

    return make_response_object(product_response)
