from app.config import orm_database
from app.config.orm_models import User
from app.config.repositories import UserRepository
from app.controllers.user import UserHandler
from app.services.user import UserService
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..config import database
from sqlalchemy.orm import Session
from .. import schemas, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model= schemas.Token)
def login(db: Session = Depends(orm_database.get_db), user_credentials: OAuth2PasswordRequestForm = Depends()):
    # conn, cursor = database.Database().connect()
    # cursor.execute("""SELECT id,email,password FROM users WHERE email = %s""", [user_credentials.username])
    # user = cursor.fetchone()

    user_repo = UserRepository(session=db, model=User)
    user_service = UserService(user_repo)
    user_handler = UserHandler(user_service)

    user = user_handler.get_user_by_email(user_credentials.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not oauth2.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    #create a token

    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    token_type = "Bearer"
    # return token

    return {"access_token" : access_token, "token_type": token_type}
