from typing import Optional
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import ClassifyGoods
from sqlalchemy import update

from ..schemas import ClassifyGoodsCreate, ClassifyGoodsUpdate


class CRUDClassifyGoods(CRUDBase[ClassifyGoods, ClassifyGoodsCreate, ClassifyGoodsUpdate]):
    @staticmethod
    def get_classify_goods_by_product_id(db: Session, product_id: str):
        current_classify_goods = db.query(ClassifyGoods).filter(ClassifyGoods.product_id == product_id).first()
        return current_classify_goods

    @staticmethod
    def get_classify_goods_by_id(db: Session, classify_goods_id: str) -> Optional[ClassifyGoods]:
        current_classify_goods = db.query(ClassifyGoods).get(classify_goods_id)
        return current_classify_goods

    def update_data(self, db: Session, current_classify_goods: ClassifyGoods, data: dict):
        update_stmt = update(self.model).where(self.model.id == current_classify_goods.id).values(
            data=data)
        db.execute(update_stmt)


crud_classify_goods = CRUDClassifyGoods(ClassifyGoods)
