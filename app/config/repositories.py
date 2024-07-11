# repositories.py
from sqlalchemy.orm import Session
from .orm_models import Investment

class InvestmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, investment: Investment):
        self.session.add(investment)
        self.session.commit()
        return investment

    def get_by_id(self, investment_id: int) -> Investment:
        return self.session.query(Investment).filter(Investment.id == investment_id).one()
    
    def get_all(self, search_filter=None):
        query = self.session.query(Investment)
        if search_filter:
            query = query.filter(Investment.type == search_filter)  # Aplica filtro adicional si es necesario

        return query.all()

    def remove(self, investment_id: int):
        investment = self.session.query(Investment).filter(Investment.id == investment_id).one()
        self.session.delete(investment)
        self.session.commit()