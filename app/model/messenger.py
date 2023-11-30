from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, text, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.model.base import Base


class Messenger(Base):
    __tablename__ = 'messenger'

    id = Column(String(255), primary_key=True, nullable=False)
    sender_id = Column(String(255), ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    receiver_id = Column(String(255), ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    content = Column(String(500), nullable=True)
    is_read = Column(Boolean, nullable=False, server_default=text("false"))
    data = Column(JSON(), nullable=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

    # Relationship
    sender = relationship('User', back_populates='sent_messages', foreign_keys=[sender_id])
    receiver = relationship('User', back_populates='received_messages', foreign_keys=[receiver_id])
