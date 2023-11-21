from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.model.base import Base


class TransactionFM(Base):
    __tablename__ = 'transaction_fm'

    id = Column(String(255), primary_key=True, nullable=False)
    tx_hash = Column(Text(), nullable=True)
    status = Column(String(255), nullable=True)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)
    receiver = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    order_by = Column(String(255), nullable=False)
    is_choose = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(String(255), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

    user = relationship('User', back_populates='transaction_fm')
    product = relationship('Product', back_populates='transaction_fm', passive_deletes=True)
    product_manufacturer = relationship('ProductManufacturer', back_populates='transactions_fm', passive_deletes=True)
