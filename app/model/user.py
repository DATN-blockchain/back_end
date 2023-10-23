from sqlalchemy import (Boolean, Column, Date, String, text, JSON, func, TIMESTAMP, Float)
from sqlalchemy.orm import relationship

from app.model.base import Base, UserSystemRole, ConfirmStatusUser
from app.model.product import Product

class User(Base):
    __tablename__ = "user"

    id = Column(String(255), primary_key=True)
    username = Column(String(42), nullable=False)
    full_name = Column(String(42), nullable=True)
    avatar = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False)
    address_wallet = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default=text("false"))
    private_key = Column(String(255), nullable=True)
    address_real = Column(String(255), nullable=True)
    hashed_data = Column(String(255), nullable=True)
    birthday = Column(Date, nullable=True)
    hashed_password = Column(String(255), nullable=True)
    verify_code = Column(String(255), nullable=True)
    system_role = Column(String(255), nullable=False, default=UserSystemRole.MEMBER)
    confirm_status = Column(String(255), nullable=False, default=ConfirmStatusUser.NONE)
    survey_data = Column(JSON())
    qr_code = Column(String(255), nullable=True)
    account_balance = Column(Float(), default=5)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    products = relationship("Product", back_populates="user", passive_deletes=True)
    comments = relationship("Comment", back_populates="user", passive_deletes=True)
    reply_comments = relationship("ReplyComment", back_populates="user", passive_deletes=True)
    notifications = relationship("Notification", back_populates="user", passive_deletes=True)
    financial_transactions = relationship("FinancialTransaction", back_populates="user", passive_deletes=True)
    # transactions_fm = relationship("TransactionFM", back_populates="user", passive_deletes=True)
    # transactions_sf = relationship("TransactionSF", back_populates="user", passive_deletes=True)
    # marketplace = relationship("Marketplace", back_populates="user", passive_deletes=True)
