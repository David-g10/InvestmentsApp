from app.interfaces.user import IUser
from fastapi import status, HTTPException


class UserHandler():

    def __init__(self, user_service: IUser) -> None:
        self.user_service = user_service
    
    def get_user_by_email(self, user_email):
        try:
            user = self.user_service.get_user_by_email(user_email)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"Fallo encontrando el usuario con el email: {user_email}: {e}")
 
        # Verificar si la inversión existe
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"user with email: {user_email} was not found.")

        return user


