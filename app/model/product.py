from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.model.base import Base


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
    created_by = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

    user = relationship('User', backref='products')
    transactions_fm = relationship('TransactionFM', backref='product', passive_deletes=True)
    transactions_sf = relationship('TransactionSF', backref='product', passive_deletes=True)
    product_manufacturers = relationship('ProductManufacturer', backref='product', passive_deletes=True)
    product_farmers = relationship('ProductFarmer', backref='product', passive_deletes=True)
    marketplace = relationship('Marketplace', backref='product', passive_deletes=True)
