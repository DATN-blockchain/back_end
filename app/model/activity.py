from sqlalchemy import (Column, String, text, JSON, func, TIMESTAMP, ForeignKey)
from sqlalchemy.orm import relationship

from .base import Base


class Activity(Base):
    __tablename__ = "activity"

    id = Column(String(255), primary_key=True)
    data = Column(JSON, nullable=True)
    product_id = Column(String(255), ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    # relationship
    # product = relationship("Product", back_populates="activities", passive_deletes=True)
    # user = relationship("User", back_populates="activities", passive_deletes=True)
