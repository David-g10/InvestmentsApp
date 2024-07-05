from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..config import database
from .. import schemas, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    conn, cursor = database.Database().connect()
    cursor.execute("""SELECT id,email,password FROM users WHERE email = %s""", [user_credentials.username])
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    #create a token

    access_token = oauth2.create_access_token(data = {"user_id" : user["id"]})
    token_type = "Bearer"
    # return token

    return {"access_token" : access_token, "token_type": token_type}
