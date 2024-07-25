from fastapi import status, HTTPException

from ..interfaces.investment_interface import IInvestment

class InvestmentHandler():

    def __init__(self, investment_service: IInvestment) -> None:
        self.investment_service = investment_service

    def add(self, *args):
        try:
            print(*args)
            new_stock_investment = self.investment_service.add_investment(*args)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"Error al guardar en la base de datos: {str(e)}") from e
        return new_stock_investment
        
    
    def close(self):
        return self.investment_service.close_investment()

    def delete(self):
        return self.investment_service.delete_investment()
    
    def get_by_id(self):
        return self.investment_service.get_investment_by_id()
    
    def get_all(self, search_filter=None):
        investments =  self.investment_service.get_investments(search_filter)

        if not investments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No Investments found.")
        return investments    

