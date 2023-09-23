from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.model.base import Base


class ProductFarmer(Base):
    __tablename__ = 'product_farmer'

    id = Column(String(255), primary_key=True, nullable=False)
    product_id = Column(String(255), ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    transaction_sf_id = Column(String(255), ForeignKey('transaction_sf.id', ondelete='CASCADE'), nullable=False)

    product = relationship('Product', backref='products_farmers')
    transaction_sf = relationship('TransactionSF', backref='products_farmer')
