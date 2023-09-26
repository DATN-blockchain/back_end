import logging
from fastapi import APIRouter
from fastapi import Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.utils.response import make_response_object
import cloudinary.uploader
from app.core.settings import settings
from app.constant.template import NotificationTemplate

from app.schemas.product import ProductCreateParams, ProductUpdate
from app.model.base import ProductType, ProductRole, NotificationType, ProductStatus
from app.model import User, Product
from app.services import ProductService

# logger = logging.getLogger(__name__)

router = APIRouter()

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
)


@router.get("/product/list")
async def list_product(
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
        skip=0,
        limit=10):
    product_service = ProductService(db=db)

    product_response = await product_service.list_product(skip=skip, limit=limit)
    return make_response_object(product_response)


@router.get("/product/me")
async def get_product_by_me(skip=0, limit=10,
                            user: User = Depends(oauth2.get_current_user),
                            db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_response = await product_service.get_product_by_me(user_id=user.id, skip=skip, limit=limit)
    return make_response_object(product_response)


@router.get("/product/{product_id}")
async def get_product_by_id(product_id: str,
                            user: User = Depends(oauth2.get_current_user),
                            db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_response = await product_service.get_product_by_id(product_id=product_id)
    return make_response_object(product_response)


@router.post("/product/create")
async def create_product(name: str,
                         price: int = None,
                         quantity: int = None,
                         description: str = None,
                         transaction_id: str = None,
                         banner: UploadFile = File(...),
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_create = ProductCreateParams(name=name, description=description, price=price, quantity=quantity)

    product_response = await product_service.create_product(user_id=user.id,
                                                            transaction_id=transaction_id,
                                                            product_create=product_create,
                                                            banner=banner)

    return make_response_object(product_response)


@router.put("/product/update/{product_id}")
async def update_product(product_id: str,
                         name: str = None,
                         description: str = None,
                         price: str = None,
                         quantity: str = None,
                         hashed_data: str = None,
                         banner: UploadFile = File(None),
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    # authorization
    await product_service.has_product_permissions(user_id=user.id, product_id=product_id)
    product_update = ProductUpdate(name=name, description=description, price=price, quantity=quantity,
                                   hashed_data=hashed_data)

    product_response = await product_service.update_product(product_id=product_id,
                                                            product_update=product_update,
                                                            banner=banner)

    return make_response_object(product_response)


@router.put("/product/{product_id}/status")
async def update_product_status(product_id: str,
                                product_status: ProductStatus,
                                user: User = Depends(oauth2.get_current_user),
                                db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    # authorization
    await product_service.has_product_permissions(user_id=user.id, product_id=product_id)

    product_response = await product_service.update_product_status(product_id=product_id, product_status=product_status)
    return make_response_object(product_response)


@router.put("/product/{product_id}/purchase")
async def purchase_product(product_id: str,
                           price: int,
                           quantity: int,
                           user: User = Depends(oauth2.get_current_user),
                           db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_response = await product_service.purchase_product(user_id=user.id,
                                                              product_id=product_id,
                                                              price=price,
                                                              quantity=quantity)
    return make_response_object(product_response)


@router.delete("/product/{product_id}/delete")
async def delete_product(product_id: str,
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    # authorization
    await product_service.has_product_permissions(user_id=user.id, product_id=product_id)

    product_response = await product_service.delete_product(product_id=product_id)
    return make_response_object(product_response)
