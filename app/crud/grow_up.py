import logging
from datetime import date, datetime

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import CRUDBase
from ..model import GrowUp

from ..schemas import GrowUpCreate, GrowUpUpdate

logger = logging.getLogger(__name__)


class CRUDGrowUp(CRUDBase[GrowUp, GrowUpCreate, GrowUpUpdate]):
    @staticmethod
    def get_grow_up_by_id(db: Session, grow_up_id: str) -> Optional[GrowUp]:
        current_grow_up = db.query(GrowUp).get(grow_up_id)
        return current_grow_up

    @staticmethod
    def get_grow_up_by_product_farmer_id(db: Session, product_farmer_id: str, from_date: date = None,
                                         to_date: date = None, skip: int = None, limit: int = None):
        db_query = db.query(GrowUp).filter(GrowUp.product_farmer_id == product_farmer_id)
        if from_date and to_date:
            from_datetime = datetime.combine(from_date, datetime.min.time())
            to_datetime = datetime.combine(to_date, datetime.max.time())
            db_query = db_query.filter(GrowUp.created_at >= from_datetime, GrowUp.created_at <= to_datetime)
        total_grow_up = db_query.count()
        if skip and limit:
            list_grow_up = db_query.order_by(desc(GrowUp.created_at)).offset(skip).limit(limit).all()
        else:
            list_grow_up = db_query.order_by(desc(GrowUp.created_at)).all()
        return total_grow_up, list_grow_up


crud_grow_up = CRUDGrowUp(GrowUp)
