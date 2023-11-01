from sqlalchemy import Column, String, Integer, TIMESTAMP, text, func, ForeignKey
from sqlalchemy.orm import relationship

from app.model.base import Base


class Leaderboard(Base):
    __tablename__ = "leaderboard"
    id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    number_of_sales = Column(Integer(), nullable=False, default=0)
    quantity_sales = Column(Integer(), nullable=False, default=0)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"),
                        onupdate=func.current_timestamp())

    user = relationship("User", back_populates="leaderboards")
