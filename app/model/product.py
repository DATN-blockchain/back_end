from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, text, Text
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
    tx_hash = Column(Text(), nullable=True)
    product_status = Column(String(255), nullable=False)
    product_type = Column(String(255), nullable=False)
    number_of_sales = Column(Integer, nullable=False, default=0)
    view = Column(Integer, nullable=False, default=0)
    is_sale = Column(Boolean, server_default=text("false"))
    soft_delete = Column(Boolean, server_default=text("false"))
    created_by = Column(String(255), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

    user = relationship('User', back_populates='products')
    transaction_fm = relationship('TransactionFM', back_populates='product', passive_deletes=True)
    transaction_sf = relationship('TransactionSF', back_populates='product', passive_deletes=True)
    product_manufacturers = relationship('ProductManufacturer', back_populates='product', passive_deletes=True)
    product_farmers = relationship('ProductFarmer', back_populates='product', passive_deletes=True)
    marketplace = relationship('Marketplace', back_populates='product', passive_deletes=True)
    carts = relationship('Cart', back_populates='product', passive_deletes=True)
    detail_description = relationship('DetailDescription', back_populates='product', passive_deletes=True)
    classify_goods = relationship('ClassifyGoods', back_populates='product', passive_deletes=True)
