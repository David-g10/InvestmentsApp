from abc import ABC, abstractmethod


#TODO: add the input params as services methods.
class IUser(ABC):

    @abstractmethod
    def get_user_by_email(self, user_email):
        pass
