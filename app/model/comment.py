from sqlalchemy import (Column, String, text, func, TIMESTAMP, ForeignKey)
from sqlalchemy.orm import relationship

from app.model.base import Base


class Comment(Base):
    __tablename__ = "comment"

    id = Column(String(255), primary_key=True)
    content = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    marketplace_id = Column(String(255), ForeignKey("marketplace.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    # Relationship
    user = relationship("User", back_populates="comments")
    marketplace = relationship("Marketplace", back_populates="comments")
    reply_comments = relationship("ReplyComment", back_populates="comment", passive_deletes=True)
