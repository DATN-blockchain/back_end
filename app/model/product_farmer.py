from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.model.base import Base
from app.model.product import Product
from app.model.transaction_sf import TransactionSF



class ProductFarmer(Base):
    __tablename__ = 'product_farmer'

    id = Column(String(255), primary_key=True, nullable=False)
    product_id = Column(String(255), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    transaction_sf_id = Column(String(255), ForeignKey('transaction_sf.id', ondelete='CASCADE'), nullable=False)
    #
    product = relationship('Product', back_populates='product_farmers')
    transactions_sf = relationship('TransactionSF', back_populates='product_farmer')
