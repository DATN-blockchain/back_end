from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.model.base import Base
from app.model.base import Base


class Marketplace(Base):
    __tablename__ = 'marketplace'

    id = Column(String(255), primary_key=True, nullable=False)
    hashed_data = Column(String(255), nullable=True)
    order_type = Column(String(255), nullable=False)
    order_id = Column(String(255), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    order_by = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

    # product = relationship('Product', back_populates='marketplace')
    # user = relationship('User', back_populates='marketplace')
