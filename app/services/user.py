from app.interfaces.user import IUser
from ..config.repositories import UserRepository

class UserService(IUser):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def get_user_by_email(self, user_email):
        return self.user_repository.get_by_email(user_email)
