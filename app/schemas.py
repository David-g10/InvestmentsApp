from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class InvestmentBase(BaseModel):
    investment_name: str
    token: Optional[str] = None
    amount: float

class CreateInvestment(InvestmentBase):
    pass

class UpdateInvestment(BaseModel):
    amount: float

class ResponseModelInvestment(InvestmentBase):
    id: int    
    opening_at: datetime

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
    