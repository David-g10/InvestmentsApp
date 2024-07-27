from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy import inspect


db_host = settings.DATABASE_HOST
db_name = settings.DATABASE_NAME
db_user = settings.DATABASE_USER
db_password = settings.DATABASE_PASSWORD


SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def obj_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

def flatten_join(tup_list):
    flattened_list = []
    for a, b in tup_list:
        dict_a = obj_to_dict(a)
        dict_b = obj_to_dict(b)
        
        # Handle key duplication by creating a new dictionary for dict_b with renamed keys
        dict_b_renamed = {}
        for key in dict_b:
            new_key = f"{b.__class__.__name__.lower()}_{key}" if key in dict_a else key
            dict_b_renamed[new_key] = dict_b[key]
        
        merged_dict = {**dict_a, **dict_b_renamed}
        flattened_list.append(merged_dict)
    return flattened_list
