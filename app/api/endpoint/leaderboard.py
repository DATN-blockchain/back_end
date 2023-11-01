from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

from app.db.database import get_db
from app.model import User
from app.services.leaderboard import LeaderboardService
from app.utils.response import make_response_object
from app.api.depend import oauth2

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/leaderboard")
async def get_leaderboard(limit: int = 10, db: Session = Depends(get_db),
                          user: User = Depends(oauth2.get_current_user)):
    logger.info("Endpoints: get_leaderboard called.")
    service = LeaderboardService(db=db)
    leaderboard_response = await service.get_leaderboard(limit=limit)
    logger.info("Endpoints: get_leaderboard called successfully.")
    return make_response_object(leaderboard_response)
