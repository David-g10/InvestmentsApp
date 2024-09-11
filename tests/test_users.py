import pytest
from jose import jwt
from app import schemas
from app.config.config import settings

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

def test_get_user(client, test_user):
    id = test_user["id"]
    res = client.get(f"/users/{id}")
    print(res.json())
    assert res.status_code == 200

def test_login_user(client, test_user):
    res = client.post('/login', data={'username': test_user['email'], 'password':test_user['password']})
    print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id: str =  payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "Bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@example.com', "1234", 403),
    ('wrongemail2@example.com', "wrong1234", 403),
    (None, "1234", 422),
    ('wrongemail@example.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={'username': email, 'password': password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid credentials"