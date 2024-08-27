from pydantic import BaseSettings

class Settings(BaseSettings):

    POSTGRES_DB : str  
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str

    DATABASE_HOST : str
    DATABASE_NAME : str
    DATABASE_USER : str
    DATABASE_PASSWORD : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    class Config:
        env_file = ".env"

settings = Settings()