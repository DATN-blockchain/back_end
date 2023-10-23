from typing import Optional

from pydantic import BaseModel

from app.schemas import UserInfo


# from app.schemas import UserInfo


class FinancialTransactionBase(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    status: Optional[str] = None
    type_transaction: Optional[str] = None
    amount: Optional[int] = None
    transaction_code: Optional[str] = None


class FinancialTransactionCreate(FinancialTransactionBase):
    pass


class FinancialTransactionUpdate(BaseModel):
    status: Optional[str] = None


class FinancialTransactionResponse(FinancialTransactionBase):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    user: Optional[UserInfo] = None
