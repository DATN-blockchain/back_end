from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.model.base import Base


class GrowUp(Base):
    __tablename__ = 'grow_up'

    id = Column(String(255), primary_key=True)
    image = Column(String(255), nullable=True)
    video = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    tx_hash = Column(Text(), nullable=True)
    product_farmer_id = Column(String(255), ForeignKey('product_farmer.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

    product_farmer = relationship("ProductFarmer", back_populates="grow_ups")
