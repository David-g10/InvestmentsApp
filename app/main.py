from fastapi import FastAPI
from .routers import investment,user, auth

app = FastAPI()

app.include_router(investment.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to my investments API."}