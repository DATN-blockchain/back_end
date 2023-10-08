import logging

from sqlalchemy.orm import Session
from sqlalchemy import desc

from .base import CRUDBase
from ..model import Activity
from ..schemas import ActivityCreate, ActivityUpdate

logger = logging.getLogger(__name__)


class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):

    @staticmethod
    def create_activity(db: Session, *, create_activity: ActivityCreate) -> Activity:
        logger.info("CRUDUserProject: create_activity called.")
        create_activity = Activity(**create_activity.dict())
        db.add(create_activity)
        db.commit()
        db.refresh(create_activity)
        logger.info("CRUDUserProject: create_activity called successfully.")
        return create_activity

    @staticmethod
    def get_activity_by_id(db: Session, product_id: str, user_id: str):
        logger.info("CRUDUserProject: get_activity_by_id called.")
        result = db.query(Activity).filter(Activity.product_id == product_id,
                                           Activity.user_id == user_id).first()

        logger.info("CRUDUserProject: get_activity_by_id called successfully.")
        return result

    @staticmethod
    def get_activities_by_product(db: Session, product_id: str, skip: int, limit: int):
        logger.info("CRUDUserProject: get_activities called.")
        db_query = db.query(Activity)
        if not product_id:
            db_query = db_query
        else:
            db_query = db_query.filter(Activity.product_id == product_id)
        total_activities = db_query.count()
        list_activities = db_query.order_by(desc(Activity.created_at)).offset(skip).limit(limit).all()

        logger.info("CRUDUserProject: get_activities called successfully.")
        return total_activities, list_activities

    @staticmethod
    def get_activities_by_user(db: Session, user_id: str, skip: int, limit: int):
        logger.info("CRUDUserProject: get_activities_by_user called.")
        db_query = db.query(Activity).filter(Activity.user_id == user_id)
        total_activities = db_query.count()
        list_activities = db_query.order_by(desc(Activity.created_at)).offset(skip).limit(limit).all()

        logger.info("CRUDUserProject: get_activities_by_user called successfully.")
        return total_activities, list_activities


crud_activity = CRUDActivity(Activity)
