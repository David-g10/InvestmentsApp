from app import schemas
from fastapi import status, HTTPException, APIRouter
from ..config import database
from .. import oauth2

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseModelUser)
def create_user(user: schemas.CreateUser):
    conn, cursor = database.Database().connect()
    #hashing the password
    hashed_password = oauth2.hash_password(user.password)
    user.password = hashed_password

    cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING * """,
                  (user.name, user.email, user.password))
    new_user = cursor.fetchone()
    conn.commit()

    return new_user

@router.get('/') #, status_code=status.HTTP_200_OK
def get_users():
    conn, cursor = database.Database().connect()
    cursor.execute("""SELECT id,name,email,created_at FROM users""")
    users = cursor.fetchall()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"users were not found.")
    return users

@router.get('/{id}')
def get_user(id: int):
    conn, cursor = database.Database().connect()
    cursor.execute("""SELECT id,name,email,created_at FROM users WHERE id = %s""", [str(id)])
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found.")
    return user
