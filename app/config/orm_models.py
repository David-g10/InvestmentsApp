from .orm_database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime

class Investments(Base):
    __tablename__ = "investment_orm"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    investment_name = Column(String, nullable=False)
    token =  Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    opening_at = Column(DateTime, nullable=False)
    