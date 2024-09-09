# repositories.py
from sqlalchemy.orm import Session

from app.config.orm_database import obj_to_dict

class BaseRepository:
    def __init__(self, session: Session, model):
        self.session = session
        self.model = model

    def add(self, entity):
        self.session.add(self.entity)
        self.session.commit()
        return entity

         
    def get_by_id(self, entity_id: int):
        query = self.session.query(self.model).filter(self.model.id == entity_id).one()
        return query
    
    def get_all(self, search_filter=None):
        query = self.session.query(self.model)
        
        if search_filter:
            query = query.filter(self.model.type == search_filter)  # Aplica filtro adicional si es necesario
            
        return query.all()

    def remove(self, entity_id: int):
        entity = self.session.query(self.model).filter(self.model.id == entity_id).one()

        print(obj_to_dict(entity))
        self.session.delete(entity)
        self.session.commit()


    def join_query(self, other_model, on_clause, *columns):
        if columns:
            query = self.session.query(*columns).select_from(self.model).join(other_model, on_clause)
        else:
            query = self.session.query(self.model, other_model).select_from(self.model).join(other_model, on_clause)
        return query

class InvestmentRepository(BaseRepository):
    def __init__(self, session: Session, model):
        super().__init__(session, model)