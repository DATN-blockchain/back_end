from typing import Optional

from pydantic import BaseModel


class ActivityBase(BaseModel):
    id: Optional[str] = None
    data: Optional[str] = None
    user_id: Optional[str] = None
    product_id: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    pass
