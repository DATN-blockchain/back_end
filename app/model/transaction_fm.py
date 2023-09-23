from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.model.base import Base


class TransactionFM(Base):
    __tablename__ = 'transaction_fm'

    id = Column(String(255), primary_key=True, nullable=False)
    hashed_data = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)
    user_id = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(String(255), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

    # user = relationship('User', back_populates='transactions_fm')
    # product = relationship('Product', back_populates='transactions_fm', passive_deletes=True)
    # product_manufacturer = relationship('ProductManufacturer', back_populates='transactions_fm', passive_deletes=True)
