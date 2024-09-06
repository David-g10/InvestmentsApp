# Special file that pytest uses, it allow us to define fixtures here.
# Any fixture you define here will automatically be accesable to any test on this package. 
# Anything within the test package even subpackages will have acces to the fixtures defined on this file.

# scope arg define how the fixture will be executed or the frequency of it, per function call, module, session, class, etc.
from fastapi.testclient import TestClient
from app.main import app
from app.config.orm_database import get_db, Base
import pytest

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from app.config.config import settings


db_host = settings.DATABASE_HOST
db_name = settings.DATABASE_NAME
db_user = settings.DATABASE_USER
db_password = settings.DATABASE_PASSWORD
db_env = settings.ENV

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}_{db_env}" if db_env else f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    # run out code before we run our test
    # Dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run our code after our test finishes

@pytest.fixture
def test_user(client):
    user_data = {"name":"yaz","email":"yaz@example.com", "password":"1234"}
    res = client.post('/users/', json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user