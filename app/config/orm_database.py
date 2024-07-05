from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

db_host = settings.DATABASE_HOST
db_name = settings.DATABASE_NAME
db_user = settings.DATABASE_USER
db_password = settings.DATABASE_PASSWORD


SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Base.metadata.create_all(bind=engine) #This line will create the tables on Db if they doesnt exist.

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
