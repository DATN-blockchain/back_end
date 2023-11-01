from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas import UserInfo


class LeaderboardBase(BaseModel):
    id: Optional[str] = None
    number_of_sales: Optional[int] = 0
    quantity_sales: Optional[int] = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class LeaderboardCreate(LeaderboardBase):
    user_id: Optional[str] = None


class LeaderboardUpdate(LeaderboardBase):
    number_of_sales: Optional[int] = None
    quantity_sales: Optional[int] = None


class LeaderboardResponse(LeaderboardBase):
    user: Optional[UserInfo] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
