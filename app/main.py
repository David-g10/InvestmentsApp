from fastapi import FastAPI, Depends
from .routers import investment,user, auth
from sqlalchemy.orm import Session
from .config.orm_database import get_db
from .config import orm_models
from .config.orm_database import engine

orm_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(investment.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to my investments API."}

@app.get("/ormtest")
def test(db: Session = Depends(get_db)):
    return {"db conection:": "success"}
