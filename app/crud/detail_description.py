from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .base import CRUDBase
from ..model import DetailDescription

from ..schemas import DetailDescriptionCreate, DetailDescriptionUpdate


class CRUDDetailDescription(CRUDBase[DetailDescription, DetailDescriptionCreate, DetailDescriptionUpdate]):
    @staticmethod
    def get_detail_description_by_product_id(db: Session, product_id: str):
        current_detail_description = db.query(DetailDescription).filter(DetailDescription.product_id == product_id).all()
        return current_detail_description

    @staticmethod
    def get_detail_description_id(db: Session, detail_description_id: str) -> Optional[DetailDescription]:
        current_detail_description = db.query(DetailDescription).get(detail_description_id)
        return current_detail_description

    @staticmethod
    def list_detail_description(db: Session, skip: int, limit: int, product_id: str):
        db_query = db.query(DetailDescription).filter(DetailDescription.product_id == product_id)
        total_detail_description = db_query.count()
        list_detail_description = db_query.order_by(desc(DetailDescription.created_at)).offset(skip).limit(limit).all()
        return total_detail_description, list_detail_description


crud_detail_description = CRUDDetailDescription(DetailDescription)
