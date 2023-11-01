import logging
from typing import Union, Any, Dict, Tuple

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.crud import CRUDBase
from app.model import Leaderboard
from app.schemas.leaderboard import LeaderboardCreate, LeaderboardUpdate

logger = logging.getLogger(__name__)


class CRUDLeaderboard(CRUDBase[Leaderboard, LeaderboardCreate, LeaderboardUpdate]):

    @staticmethod
    def get_leaderboard(db: Session, limit: int):
        logger.info("CRUDLeaderboard: get_leaderboard_in_product called.")
        db_query = (db.query(Leaderboard).filter(Leaderboard.number_of_sales > 0).
                    order_by(desc(Leaderboard.number_of_sales)).limit(limit).all())
        logger.info("CRUDLeaderboard: get_leaderboard_in_product called successfully.")
        return db_query

    @staticmethod
    def get_leaderboard_by_user_id(db: Session, user_id: str):
        result = db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
        return result

    @staticmethod
    def delete(db: Session, *, leaderboard_id: str) -> Leaderboard:
        logger.info("CRUDTask: delete called.")
        current_leaderboard = self.get(db, entry_id=leaderboard_id)
        if not current_leaderboard:
            logger.info("CRUDTask: delete called failed")
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_LEADERBOARD_NOT_FOUND)
        else:
            db.delete(current_leaderboard)
            db.commit()
            deleted_task = current_leaderboard
            logger.info("CRUDTask: delete called successfully.")
            return deleted_task


crud_leaderboard = CRUDLeaderboard(Leaderboard)
