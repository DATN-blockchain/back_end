import logging

from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..depend import oauth2
from ...model import User
from ...services import ActivityService
from ...db.database import get_db
from ...utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/activities/product")
async def get_activities_by_product(
        product_id: str = None,
        skip: int = 0,
        limit: int = 10,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
) -> Any:
    activity_service = ActivityService(db=db)
    logger.info(f"Endpoints: get_activities_by_product with uid {user.id} called.")

    activity_response = await activity_service.get_activities_by_product(product_id=product_id,
                                                                         skip=skip, limit=limit)
    logger.info("Endpoints: get_activities_by_product called successfully.")
    return make_response_object(activity_response)


@router.get("/activities/{user_id}/user")
async def get_activities_by_user(
        skip: int = 0,
        limit: int = 10,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
) -> Any:
    activity_service = ActivityService(db=db)
    logger.info(f"Endpoints: get_activities_by_user with uid {user.id} called.")

    activity_response = await activity_service.get_activities_by_user(user_id=user.id, skip=skip, limit=limit)
    logger.info("Endpoints: get_activities_by_user called successfully.")
    return make_response_object(activity_response)
