from .orm_database import Base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey, func, Enum, text
from sqlalchemy.orm import relationship
import enum


class InvestmentIncomeType(enum.Enum):
    FIJA = "FIJA"
    VARIABLE = "VARIABLE"

class InvestmentType(enum.Enum):
    BURSATIL = "BURSATIL"
    CDT = "CDT"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}  # Omitir si no estás usando esquemas
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    phone_number = Column(String, nullable=True)

    investments = relationship("Investment", back_populates="user")


class Investment(Base):
    __tablename__ = "investments"
    __table_args__ = {"schema": "public"}  # Omitir si no estás usando esquemas

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    opening_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    closed_at = Column(TIMESTAMP(timezone=True))
    income_type = Column(Enum(InvestmentIncomeType), nullable=False)
    status = Column(String, server_default="OPEN")
    type = Column(Enum(InvestmentType), nullable=False)
    user_id = Column(Integer, ForeignKey('public.users.id', ondelete='CASCADE'), nullable=False)

    user = relationship("User", back_populates="investments")
    stock = relationship("StockMarketInvestment", back_populates="investment")

class StockMarketInvestment(Base):
    __tablename__ = "stock_market_investments"
    __table_args__ = {"schema": "public"}  # Omitir si no estás usando esquemas

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False)
    shares = Column(Float, nullable=False)
    broker = Column(String)
    commission = Column(Float, nullable=True, server_default=text('0.0'))
    investment_id = Column(Integer, ForeignKey('public.investments.id', ondelete='CASCADE'), nullable=False)

    investment = relationship("Investment", back_populates="stock")


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = {"schema": "public"}  # Omitir si no estás usando esquemas
    user_id = Column(
        Integer,
        ForeignKey("public.users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    investment_id = Column(
        Integer,
        ForeignKey("public.investments.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
