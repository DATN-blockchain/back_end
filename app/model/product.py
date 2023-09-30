from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.model.base import Base
from app.model.transaction_fm import TransactionFM

class Product(Base):
    __tablename__ = 'product'

    id = Column(String(255), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    banner = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=True)
    hashed_data = Column(String(255), nullable=True)
    product_status = Column(String(255), nullable=False)
    product_type = Column(String(255), nullable=False)
    created_by = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

    user = relationship('User', back_populates='products')
    transactions_fm = relationship('TransactionFM', back_populates='product', passive_deletes=True)
    transaction_sf = relationship('TransactionSF', back_populates='product', passive_deletes=True)
    # product_manufacturers = relationship('ProductManufacturer', back_populates='product', passive_deletes=True)
    product_farmers = relationship('ProductFarmer', back_populates='product', passive_deletes=True)
    marketplace = relationship('Marketplace', back_populates='product', passive_deletes=True)
