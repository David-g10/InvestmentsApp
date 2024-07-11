from abc import ABC, abstractmethod

class IInvestment(ABC):

    @abstractmethod
    def add_investment():
        pass

    @abstractmethod    
    def close_investment():
        pass

    @abstractmethod
    def delete_investment():
        pass

    @abstractmethod
    def get_investment_by_id():
        pass

    @abstractmethod
    def get_investments(search_filter=None):
        pass