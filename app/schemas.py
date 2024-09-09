from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from .config.orm_models import InvestmentType, InvestmentIncomeType


class InvestmentBase(BaseModel):
    amount: float
    income_type: InvestmentIncomeType
    type: InvestmentType

class StockMarketInvestment(InvestmentBase):
    income_type: InvestmentIncomeType = InvestmentIncomeType.VARIABLE
    type:InvestmentType = InvestmentType.BURSATIL
    ticker: str
    shares: float
    broker: Optional[str] = None
    commission: Optional[float] = None

class CreateInvestment(InvestmentBase):
    pass

class CreateStockMarketInvestment(StockMarketInvestment):
    pass

class UpdateInvestment(InvestmentBase):
    closed_at: Optional[datetime]
    status: Optional[str]

class UpdateStockMarketInvestment(BaseModel):
    broker: Optional[str]

class ResponseModelInvestment(InvestmentBase):
    id: int    
    opening_at: datetime
    class Config:
        orm_mode = True

class ResponseModelStockMarketInvestment(StockMarketInvestment):
    id: int
    investment_id: int
    opening_at: datetime
    
    class Config:
        orm_mode = True
        use_enum_values = True

##################################################### users 

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str

class CreateUser(UserBase):
    pass

class ResponseModelUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

######################## votes #########################

class VoteBase(BaseModel):
    investment_id: int
    dir: conint(le=1) # type: ignore
    

    