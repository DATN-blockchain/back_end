from sqlalchemy import (Column, String, text, Integer, func, TIMESTAMP, ForeignKey, Text)
from sqlalchemy.orm import relationship

from app.model.base import Base, FinancialStatus


class FinancialTransaction(Base):
    __tablename__ = "financial_transaction"

    id = Column(String(255), primary_key=True, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(255), nullable=False, default=FinancialStatus.PENDING)
    tx_hash = Column(Text(), nullable=True)
    type_transaction = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    # relationship
    user = relationship('User', back_populates='financial_transactions')
