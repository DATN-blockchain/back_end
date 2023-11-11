from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from app.model.base import Base


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(String(255), primary_key=True, nullable=False)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)
    user_id = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(String(255), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('now()'), nullable=True)

    # relationship
    user = relationship('User', back_populates='carts', passive_deletes=True)
    product = relationship('Product', back_populates='carts', passive_deletes=True)
