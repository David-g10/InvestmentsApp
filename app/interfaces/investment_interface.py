from abc import ABC, abstractmethod


#TODO: add the input params as services methods.
class IInvestment(ABC):

    @abstractmethod
    def add_investment(self, amount, income_type):
        pass

    @abstractmethod    
    def close_investment():
        pass

    @abstractmethod
    def delete_investment(self, investment_id):
        pass

    @abstractmethod
    def get_investment_by_id(self, investment_id):
        pass

    @abstractmethod
    def get_investments(self, search_filter=None):
        pass

    @abstractmethod
    def update_investment(self, search_filter=None):
        pass