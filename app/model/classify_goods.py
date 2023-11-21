from sqlalchemy.orm import relationship
from sqlalchemy import (text, Column, String, func, TIMESTAMP, ForeignKey, JSON)


from app.model.base import Base


class ClassifyGoods(Base):
    __tablename__ = "classify_goods"

    id = Column(String(255), primary_key=True)
    data = Column(JSON())
    product_id = Column(String(255), ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    # Relationship
    product = relationship("Product", back_populates="classify_goods")
