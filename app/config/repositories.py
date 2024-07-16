# repositories.py
from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, session: Session, model):
        self.session = session
        self.model = model

    def add(self, entity):
        self.session.add(self.entity)
        self.session.commit()
        return entity

    def get_by_id(self, entity_id: int):
        return self.session.query(self.model).filter(self.model.id == entity_id).one()
    
    def get_all(self, search_filter=None):
        query = self.session.query(self.model)
        
        if search_filter:
            query = query.filter(self.model.type == search_filter)  # Aplica filtro adicional si es necesario
            
        return query.all()

    def remove(self, entity_id: int):
        entity = self.session.query(self.model).filter(self.model.id == entity_id).one()
        self.session.delete(entity)
        self.session.commit()

class InvestmentRepository(BaseRepository):
    def __init__(self, session: Session, model):
        super().__init__(session, model)