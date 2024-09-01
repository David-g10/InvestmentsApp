from app import schemas
from database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to my investments API.'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"name":"yaz","email":"yaz@example.com", "password":"1234"})
    print(res.json())
    new_user_schema = schemas.ResponseModelUser(**res.json())
    assert res.status_code == 201
    assert new_user_schema.email == "yaz@example.com"
