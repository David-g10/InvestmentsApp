from app import schemas
from fastapi import status, APIRouter, Depends, HTTPException
from typing import List
from .. import oauth2
from ..config import orm_database
from sqlalchemy.orm import Session
from ..controllers.investment import InvestmentHandler
from ..services.investment import StockMarketService
from ..config.repositories import InvestmentRepository
from ..config.orm_models import StockMarketInvestment
import logging

from app.config import orm_models

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


router = APIRouter(
    prefix="/stockinvestments",
    tags=["StockInvestments"]
)

@router.get("/stock_market", response_model=List[schemas.ResponseModelStockMarketInvestment])
def get_stock_market_investments(
    db: Session = Depends(orm_database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    
    stock_repo = InvestmentRepository(session=db, model=StockMarketInvestment)
    stock_service = StockMarketService(stock_repo)
    stock_handler = InvestmentHandler(stock_service)

    stocks_investments = stock_handler.get_all()
    
    return stocks_investments

@router.get("/{id}", response_model=schemas.ResponseModelStockMarketInvestment)
def get_stock_investment(
    id: int, 
    db: Session = Depends(orm_database.get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    stock_repo = InvestmentRepository(session=db, model=StockMarketInvestment)
    stock_service = StockMarketService(stock_repo)
    stock_handler = InvestmentHandler(stock_service)

    stocks_investment = stock_handler.get_by_id(id, current_user)

    return stocks_investment

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseModelStockMarketInvestment)
def add_stock_investment(
    investment: schemas.CreateStockMarketInvestment,
    db: Session = Depends(orm_database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    new_investment = investment.dict()

    stock_repo = InvestmentRepository(session=db, model=StockMarketInvestment)
    stock_service = StockMarketService(stock_repo)
    stock_handler = InvestmentHandler(stock_service)

    new_stock_investment = stock_handler.add(current_user['id'], *new_investment.values())
    # Devolver el objeto recién creado y guardado
    return new_stock_investment

#TODO: migrate logic to controller and service layers.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_investment(
    id: int, 
    db: Session = Depends(orm_database.get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    stock_repo = InvestmentRepository(session=db, model=StockMarketInvestment)
    stock_service = StockMarketService(stock_repo)
    stock_handler = InvestmentHandler(stock_service)
    
    stock_handler.delete(id, current_user)

@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_investment(
    id: int,
    investment_data: schemas.UpdateStockMarketInvestment,
    db: Session = Depends(orm_database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    stock_repo = InvestmentRepository(session=db, model=StockMarketInvestment)
    stock_service = StockMarketService(stock_repo)
    stock_handler = InvestmentHandler(stock_service)
    
    updated_stock_investment = stock_handler.update(id, investment_data, current_user)
    return updated_stock_investment