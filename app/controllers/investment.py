from ..interfaces.investment_interface import IInvestment

class InvestmentHandler():

    def __init__(self, investment_service: IInvestment) -> None:
        self.investment_service = investment_service

    def add(self):
        return self.investment_service.add_investment()
    
    def close(self):
        return self.investment_service.close_investment()

    def delete(self):
        return self.investment_service.delete_investment()
    
    def get_by_id(self):
        return self.investment_service.get_investment_by_id()
    
    def get_all(self, search_filter=None):
        return self.investment_service.get_investments(search_filter)

