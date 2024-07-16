from fastapi import FastAPI, Depends
from .routers import investment,user, auth, vote
from sqlalchemy.orm import Session
from .config.orm_database import get_db
from .config import orm_models
from .config.orm_database import engine

# orm_models.Base.metadata.drop_all(bind=engine)
orm_models.Base.metadata.create_all(bind=engine) #This line will create the tables on Db if they doesnt exist.

app = FastAPI()

app.include_router(investment.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to my investments API."}

@app.get("/ormtest")
def test(db: Session = Depends(get_db)):
    users = db.query(orm_models.User).all()
    return {"data": users}
