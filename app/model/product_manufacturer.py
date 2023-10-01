from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.model.base import Base
from app.model.product import Product
from app.model.transaction_fm import TransactionFM


class ProductManufacturer(Base):
    __tablename__ = 'product_manufacturer'

    id = Column(String(255), primary_key=True, nullable=False)
    product_id = Column(String(255), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    transaction_fm_id = Column(String(255), ForeignKey('transaction_fm.id', ondelete='CASCADE'), nullable=False)

    product = relationship('Product', back_populates='product_manufacturers')
    transactions_fm = relationship('TransactionFM', back_populates='product_manufacturer')
