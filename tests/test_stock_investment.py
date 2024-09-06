from app import schemas

def test_add_stock_investment(client):
    res = client.post("/stockinvestments/", json={"amount":10,"ticker":"NU", "shares":"1"})
    print(res.json())
    new_stock = schemas.ResponseModelStockMarketInvestment(**res.json())
    assert res.status_code == 201


def test_get_stock_investments(client):
    res = client.get("/stockinvestments/stock_market")
    print(res.json())
    # new_stock = List[schemas.ResponseModelStockMarketInvestment(**res.json())]
    assert res.status_code == 200
