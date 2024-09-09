from app.config.orm_database import flatten_join
from ..interfaces.investment_interface import IInvestment
from ..config.repositories import InvestmentRepository
from ..config.orm_models import Investment, StockMarketInvestment
from sqlalchemy.exc import SQLAlchemyError
from ..config.orm_database import obj_to_dict

class InvestmentService(IInvestment):
    def __init__(self, investment_repository: InvestmentRepository):
        self.investment_repository = investment_repository

    def add_investment(self, amount, income_type):
        new_investment = Investment(amount=amount, income_type=income_type)
        return self.investment_repository.add(new_investment)

    def delete_investment(self, investment_id):
        self.investment_repository.remove(investment_id)
        
    def get_investment_by_id(self, investment_id):
        return self.investment_repository.get_by_id(investment_id)
    
    def get_investments(self, search_filter=None):
        return self.investment_repository.get_all(search_filter)

    def close_investment():
        pass

class StockMarketService(IInvestment):
    def __init__(self, investment_repository: InvestmentRepository):
        self.investment_repository = investment_repository

    def add_investment(self, user_id, amount, income_type, type, ticker, shares, broker=None, commission=None):
        self.investment_repository.session.close()
        try:
            # Iniciar una transacción
            self.investment_repository.session.begin()

            # Crear y agregar la inversión general
            new_investment = Investment(user_id=user_id, amount=amount, income_type=income_type, type=type)
            self.investment_repository.session.add(new_investment)
            self.investment_repository.session.flush()  # Esto asegura que el investment.id esté disponible

            # Crear y agregar la información específica de la acción
            new_stock_investment = StockMarketInvestment(ticker=ticker, shares=shares, broker=broker, commission=commission)
            new_investment.stock = new_stock_investment
            self.investment_repository.session.add(new_stock_investment)
            # Confirmar la transacción
            self.investment_repository.session.commit()
            # Refrescar el objeto para asegurar que contiene cualquier actualización de la base de datos
            self.investment_repository.session.refresh(new_investment)            
        
            return obj_to_dict(new_investment)|obj_to_dict(new_stock_investment)
        except SQLAlchemyError as e:
            # Si hay un error, revertir la transacción
            self.investment_repository.session.rollback()
            raise e
        finally:
            self.investment_repository.session.close()



    def add_investments(self, entities_list):
        investments = []
        for entity in entities_list:
            try:
                # Iniciar una transacción
                self.investment_repository.session.begin()

                # Crear y agregar la inversión general
                new_investment = Investment(user_id=entity['user_id'], amount=entity['amount'], income_type=entity['income_type'], type=entity['type'])
                self.investment_repository.session.add(new_investment)
                self.investment_repository.session.flush()  # Esto asegura que el investment.id esté disponible
                

                # Crear y agregar la información específica de la acción
                new_stock_investment = StockMarketInvestment(ticker=entity['ticker'], shares=entity['shares'], broker=entity['broker'], commission=entity['commission'])
                new_investment.stock = new_stock_investment
                self.investment_repository.session.add(new_stock_investment)

                # Confirmar la transacción
                self.investment_repository.session.commit()
                # Refrescar el objeto para asegurar que contiene cualquier actualización de la base de datos
                self.investment_repository.session.refresh(new_investment)
                
                investments.append(obj_to_dict(new_investment)|obj_to_dict(new_stock_investment))
            except SQLAlchemyError as e:
                # Si hay un error, revertir la transacción
                self.investment_repository.session.rollback()
                raise e
            finally:
                self.investment_repository.session.close()
        return investments    

    def delete_investment(self, investment_id):
        self.investment_repository.remove(investment_id)
    
    def update_investment(self, investment_id, data):
        return self.investment_repository.update(investment_id, data)

    def get_investment_by_id(self, stock_id, flatten=True):

        # Obtener el registro por ID
        stock_market_investment = self.investment_repository.get_by_id(stock_id)

        # Realizar el join con Investment y seleccionar solo el campo user_id
        join_query = self.investment_repository.join_query(
            Investment, 
            Investment.id == stock_market_investment.investment_id
        ).filter(StockMarketInvestment.id == stock_id)

        results = join_query.all()
        if flatten:
            results = flatten_join(join_query.all())
        
        return results
    
    def get_investments(self, search_filter=None, flatten=True):
        # Realizar el join entre Investment y StockMarketInvestment
        join_query = self.investment_repository.join_query(Investment, Investment.id == StockMarketInvestment.investment_id)
        # Ejecutar la consulta y obtener los resultados
        results = join_query.all()
        if flatten:
            results = flatten_join(join_query.all())
        
        return results

    def close_investment():
        pass
