from fastapi import status, HTTPException

from ..interfaces.investment_interface import IInvestment

class InvestmentHandler():

    def __init__(self, investment_service: IInvestment) -> None:
        self.investment_service = investment_service

    def add(self, *args):
        try:
            # print(*args)
            new_stock_investment = self.investment_service.add_investment(*args)
        except Exception as e:
            # print(e)
            raise HTTPException(status_code=400, detail=f"Error al guardar en la base de datos: {str(e)}") from e
        return new_stock_investment

    def add_all(self, entities_list):
        try:
            new_stock_investments = self.investment_service.add_investments(entities_list)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail=f"Error al guardar en la base de datos: {str(e)}") from e
        return new_stock_investments    
    
    def close(self):
        return self.investment_service.close_investment()

    def delete(self, investment_id, current_user=None):
        
        investment = self.get_by_id(investment_id, current_user)
              
        self.investment_service.delete_investment(investment_id)
    
    def get_by_id(self, investment_id, current_user=None):
        try:
            investment = self.investment_service.get_investment_by_id(investment_id)[0]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Fallo encontrando la inversion con id: {id}: {e}")
 
        # Verificar si la inversión existe
        if not investment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Investment with id: {investment_id} was not found.")

        # Verificar si el usuario actual tiene permiso para ver esta inversión
        if current_user["id"] != investment["user_id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Not authorized to perform requested action.")
        return investment
    
    def get_all(self, search_filter=None, flatten=True):
        investments =  self.investment_service.get_investments(search_filter, flatten=flatten)

        if not investments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No Investments found.")
        return investments    
    
    def update(self, investment_id, data, current_user=None):
        
        investment = self.get_by_id(investment_id, current_user)         
        
        updated_investment = self.investment_service.update_investment(investment_id, data)
        return updated_investment


