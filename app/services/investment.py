from ..interfaces.investment_interface import IInvestment
from ..config.repositories import InvestmentRepository
from ..config.orm_models import Investment

class InvestmentService(IInvestment):
    def __init__(self, user_repository: InvestmentRepository):
        self.user_repository = user_repository

    def add_investment(self, username, email):
        new_user = Investment(username=username, email=email)
        return self.user_repository.add(new_user)

    def delete_investment(self, user_id):
        self.user_repository.remove(user_id)

    def get_investment_by_id(self, user_id):
        return self.user_repository.get_by_id(user_id)
    
    def get_investments(self, search_filter=None):
        return self.user_repository.get_all(search_filter)

    def close_investment():
        pass