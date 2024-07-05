from .orm_database import Base
from sqlalchemy import Column,Integer,String,Float,TIMESTAMP,ForeignKey,text, UniqueConstraint, func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"schema": "public"}  # Omitir si no estás usando esquemas
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    phone_number = Column(String, nullable=True)

    investments = relationship("Investment", back_populates="user")

class Investment(Base):
    __tablename__ = 'investments'
    __table_args__ = {"schema": "public"}  # Omitir si no estás usando esquemas
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('public.users.id', ondelete='CASCADE'), nullable=False)
    investment_name = Column(String, nullable=False)
    token = Column(String)
    amount = Column(Float, nullable=False)
    opening_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="investments")

class Vote(Base):
    __tablename__ = 'votes'
    __table_args__ = {"schema": "public"}  # Omitir si no estás usando esquemas
    user_id = Column(Integer, ForeignKey('public.users.id',
                                          ondelete='CASCADE'), primary_key=True, nullable=False)
    investment_id = Column(Integer, ForeignKey('public.investments.id',
                                          ondelete='CASCADE'), primary_key=True, nullable=False)