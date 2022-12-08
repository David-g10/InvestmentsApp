from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..config import database
from .. import schemas, utils


router = APIRouter(tags=['Authentication'])

conn, cursor = database.Database().connect()


@router.post("/login")
def login(user_credentials: schemas.UserLogin):
    
    print(user_credentials.email)
    cursor.execute("""SELECT email,password FROM users WHERE email = %s""", [user_credentials.email])
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    if not utils.verify(user_credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    #create a token

    # return token

    return {"token": "example token"}
