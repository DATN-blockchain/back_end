from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import sqlalchemy as sa

from app.model.base import Base


class DetailDescription(Base):
    __tablename__ = 'detail_description'

    id = Column(String(255), primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    image = Column(String(255), nullable=True)
    product_id = Column(String(255), ForeignKey('product.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=sa.text('now()'), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=sa.text('now()'), nullable=True)

    # relationship
    product = relationship('Product', back_populates='detail_description', passive_deletes=True)
