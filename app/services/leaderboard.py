import logging

from sqlalchemy.orm import Session
from ..crud import crud_leaderboard
from ..model.base import ProductType
from ..schemas import LeaderboardResponse

logger = logging.getLogger(__name__)


class LeaderboardService:

    def __init__(self, db: Session):
        self.db = db

    async def get_leaderboard(self, product_type: ProductType):
        logger.info("ProjectService: get_leaderboard_in_product called.")
        leaderboard = crud_leaderboard.get_leaderboard(db=self.db, product_type=product_type)
        result = [LeaderboardResponse.from_orm(item) for item in leaderboard]
        logger.info("ProjectService: get_leaderboard_in_product called successfully.")
        return result
