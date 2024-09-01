from app import schemas
from .database import client, session


def test_add_stock_investment(client):
    res = client.post("/stockinvestments/", json={"amount":10,"ticker":"NU", "shares":"1"})
    print(res.json())
    new_stock = schemas.ResponseModelStockMarketInvestment(**res.json())
    assert res.status_code == 201
