import logging
import uuid
from sqlalchemy.orm import Session

from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from ..constant.template import ActivityTemplate
from ..model import Activity, Product
from ..crud import crud_activity, crud_user, crud_product

logger = logging.getLogger(__name__)


class ActivityService:

    def __init__(self, db: Session):
        self.db = db

    async def get_activity_by_id(self, *, product_id: str, skip: int, limit: int):
        logger.info("ActivityService: get_activities called.")
        total_activities, list_activity = crud_activity.get_activity_by_id(db=self.db, product_id=product_id, skip=skip,
                                                                           limit=limit)
        result = dict(total_activities=total_activities, list_activity=list_activity)
        logger.info("ActivityService: get_activities called successfully.")
        return result

    async def get_activities_by_product(self, *, product_id: str, skip: int, limit: int):
        logger.info("ActivityService: get_activities called.")
        total_activities, list_activities = crud_activity.get_activities_by_product(db=self.db, product_id=product_id,
                                                                                    skip=skip,
                                                                                    limit=limit)
        result = dict(total_activities=total_activities, list_activities=list_activities)
        logger.info("ActivityService: get_activities called successfully.")
        return result

    async def get_activities_by_user(self, *, user_id: str, skip: int, limit: int):
        logger.info("ActivityService: get_activities_by_user called.")
        total_activities, list_activities = crud_activity.get_activities_by_user(db=self.db, user_id=user_id,
                                                                                 skip=skip,
                                                                                 limit=limit)
        result = dict(total_activities=total_activities, list_activities=list_activities)
        logger.info("ActivityService: get_activities_by_user called successfully.")
        return result

    async def create_activity(self, *, user_id: str,
                              activity_msg: ActivityTemplate.Activity_MSG,
                              activity_template: str,
                              product: Product, action: str,
                              children_name: str = None):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        logger.info("ActivityService: get_activity called.")
        if action in ['created', 'updated', 'deleted', 'claim']:
            children_name = children_name if children_name is not None else ''
            message = activity_msg(
                username=current_user.username,
                action=action,
                entity=activity_template.lower(),
                entity_name=product.name,
                children_name=children_name
            )
        elif action in ['purchase']:
            message = activity_msg(
                action=action,
                entity=activity_template.lower(),
                entity_name=product.name,
                owner=product.user.username
            )
        else:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_ACTION)

        activity_id = str(uuid.uuid4())
        activity = Activity(
            id=activity_id,
            user_id=user_id,
            data={"message": message},
            product_id=product.id
        )
        result = crud_activity.create(self.db, obj_in=activity)
        logger.info("ActivityService: get_activity called successfully.")
        return result
