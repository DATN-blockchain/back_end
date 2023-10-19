import logging
from fastapi import APIRouter, BackgroundTasks
from fastapi import Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from typing import Optional
from datetime import date

from app.schemas import GrowUpUpdate
from app.utils.background_tasks import send_notification
from app.utils.response import make_response_object
import cloudinary.uploader
from app.core.settings import settings
from app.constant.template import NotificationTemplate, ActivityTemplate

from app.schemas.product import ProductCreateParams, ProductUpdate
from app.model.base import NotificationType, ProductStatus, ActivityType
from app.model import User
from app.services import ProductService, NotificationService, ActivityService

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
        skip=0, limit=10,
        name: str = None, user_id: str = None):
    product_service = ProductService(db=db)

    product_response = await product_service.list_product(name=name, user_id=user_id, skip=skip, limit=limit)
    return make_response_object(product_response)


@router.get("/product/me")
async def get_product_by_me(skip=0, limit=10,
                            name: str = None,
                            user: User = Depends(oauth2.get_current_user),
                            db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_response = await product_service.get_product_by_me(user_id=user.id, name=name, skip=skip, limit=limit)
    return make_response_object(product_response)


@router.get("/product/{product_id}")
async def get_product_by_id(product_id: str,
                            user: User = Depends(oauth2.get_current_user),
                            db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_response = await product_service.get_product_by_id(product_id=product_id)
    return make_response_object(product_response)


@router.get("/product/{product_id}/seedling_company_history")
async def get_product_seedling_company_history(product_id: str,
                                               user: User = Depends(oauth2.get_current_user),
                                               db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_response = await product_service.get_product_seedling_company_history(product_id=product_id)
    return make_response_object(product_response)


@router.get("/product/{product_id}/farmer_history")
async def get_product_farmer_history(product_id: str,
                                     user: User = Depends(oauth2.get_current_user),
                                     db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_response = await product_service.get_product_farmer_history(product_id=product_id)
    return make_response_object(product_response)


@router.get("/product/{product_id}/history")
async def get_product_history(product_id: str,
                              user: User = Depends(oauth2.get_current_user),
                              db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_response = await product_service.get_product_history(product_id=product_id)
    return make_response_object(product_response)


@router.get("/product/{product_id}/grow_up")
async def get_product_grow_up(product_id: str,
                              skip: int = 0,
                              limit: int = 10,
                              from_date: Optional[date] = Query(default=None),
                              to_date: Optional[date] = Query(default=None),
                              user: User = Depends(oauth2.get_current_user),
                              db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    product_response = await product_service.get_product_grow_up(product_id=product_id, from_date=from_date,
                                                                 to_date=to_date, skip=skip, limit=limit)
    return make_response_object(product_response)


@router.post("/product/create")
async def create_product(name: str,
                         background_tasks: BackgroundTasks,
                         price: int = None,
                         quantity: int = None,
                         description: str = None,
                         transaction_id: str = None,
                         banner: UploadFile = File(...),
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    product_service = ProductService(db=db)
    notification_service = NotificationService(db=db)
    activity_service = ActivityService(db=db)

    product_create = ProductCreateParams(name=name, description=description, price=price, quantity=quantity)

    product_response = await product_service.create_product_entity(user_id=user.id,
                                                                   transaction_id=transaction_id,
                                                                   product_create=product_create,
                                                                   banner=banner)
    message_template = NotificationTemplate.CRUD_PRODUCT_NOTIFICATION_MSG
    background_tasks.add_task(
        send_notification, notification_service, entity=product_response,
        notification_type=NotificationType.PRODUCT_NOTIFICATION,
        message_template=message_template, action='created', current_user=user
    )
    activity_msg = ActivityTemplate.Activity_MSG
    activity_template = ActivityType.PRODUCT
    await activity_service.create_activity(user_id=user.id, activity_msg=activity_msg,
                                           activity_template=activity_template,
                                           product=product_response, action="created")

    db.refresh(product_response)
    return make_response_object(product_response)


@router.post("/product/grow_up")
async def create_grow_up(product_id: str,
                         description: str = None,
                         image: UploadFile = File(None),
                         video: UploadFile = File(None),
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    product_service = ProductService(db=db)
    activity_service = ActivityService(db=db)

    # authorization
    await product_service.has_product_permissions(user_id=user.id, product_id=product_id)

    product_response = await product_service.create_grow_up(product_id=product_id,
                                                            description=description,
                                                            image=image,
                                                            video=video)
    activity_msg = ActivityTemplate.Activity_MSG
    activity_template = ActivityType.GROW_UP
    await activity_service.create_activity(user_id=user.id, activity_msg=activity_msg,
                                           activity_template=activity_template,
                                           product=product_response.product_farmer.product, action="created")

    db.refresh(product_response)
    return make_response_object(product_response)


@router.put("/product/update/{product_id}/grow_up")
async def update_product(product_id: str,
                         grow_up_update: GrowUpUpdate,
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    # authorization
    await product_service.has_product_permissions(user_id=user.id, product_id=product_id)

    product_response = await product_service.update_grow_up(product_id=product_id, grow_up_update=grow_up_update)

    return make_response_object(product_response)


@router.put("/product/update/{product_id}")
async def update_product(product_id: str,
                         background_tasks: BackgroundTasks,
                         name: str = None,
                         description: str = None,
                         price: str = None,
                         quantity: str = None,
                         hashed_data: str = None,
                         banner: UploadFile = File(None),
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    product_service = ProductService(db=db)
    notification_service = NotificationService(db=db)
    activity_service = ActivityService(db=db)

    # authorization
    await product_service.has_product_permissions(user_id=user.id, product_id=product_id)
    product_update = ProductUpdate(name=name, description=description, price=price, quantity=quantity,
                                   hashed_data=hashed_data)

    product_response = await product_service.update_product(product_id=product_id,
                                                            product_update=product_update,
                                                            banner=banner)
    message_template = NotificationTemplate.CRUD_PRODUCT_NOTIFICATION_MSG
    background_tasks.add_task(
        send_notification, notification_service, entity=product_response,
        notification_type=NotificationType.PRODUCT_NOTIFICATION,
        message_template=message_template, action='updated', current_user=user
    )
    activity_msg = ActivityTemplate.Activity_MSG
    activity_template = ActivityType.PRODUCT
    await activity_service.create_activity(user_id=user.id, activity_msg=activity_msg,
                                           activity_template=activity_template,
                                           product=product_response, action="updated")

    return make_response_object(product_response)


@router.put("/product/{product_id}/status")
async def update_product_status(product_id: str,
                                product_status: ProductStatus,
                                user: User = Depends(oauth2.get_current_user),
                                db: Session = Depends(get_db)):
    product_service = ProductService(db=db)
    activity_service = ActivityService(db=db)

    # authorization
    await product_service.has_product_permissions(user_id=user.id, product_id=product_id)

    product_response = await product_service.update_product_status(product_id=product_id, product_status=product_status)
    activity_msg = ActivityTemplate.Activity_MSG
    activity_template = ActivityType.STATUS_PRODUCT
    await activity_service.create_activity(user_id=user.id, activity_msg=activity_msg,
                                           activity_template=activity_template,
                                           product=product_response, action="updated")
    db.refresh(product_response)
    return make_response_object(product_response)


@router.put("/product/{product_id}/purchase")
async def purchase_product(product_id: str,
                           price: int,
                           quantity: int,
                           user: User = Depends(oauth2.get_current_user),
                           db: Session = Depends(get_db)):
    product_service = ProductService(db=db)
    activity_service = ActivityService(db=db)

    product_response, current_product = await product_service.purchase_product(user_id=user.id,
                                                                               product_id=product_id,
                                                                               price=price,
                                                                               quantity=quantity)
    activity_msg = ActivityTemplate.Activity_Purchase_MSG
    activity_template = ActivityType.PRODUCT
    await activity_service.create_activity(user_id=user.id, activity_msg=activity_msg,
                                           activity_template=activity_template,
                                           product=current_product, action="purchase")
    db.refresh(product_response)
    return make_response_object(product_response)


@router.delete("/product/{product_id}/delete")
async def delete_product(product_id: str,
                         background_tasks: BackgroundTasks,
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    product_service = ProductService(db=db)

    # authorization
    await product_service.has_product_permissions(user_id=user.id, product_id=product_id)
    notification_service = NotificationService(db=db)

    product_response = await product_service.delete_product(product_id=product_id)
    message_template = NotificationTemplate.CRUD_PRODUCT_NOTIFICATION_MSG
    background_tasks.add_task(
        send_notification, notification_service, entity=product_response,
        notification_type=NotificationType.PRODUCT_NOTIFICATION,
        message_template=message_template, action='deleted', current_user=user
    )

    return make_response_object(product_response)
