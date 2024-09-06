import pytest
from app import schemas

def test_get_stock_investments(authorized_client, test_stock_investment):
    res = authorized_client.get("/stockinvestments/stock_market")

    def validate(stock):
        return schemas.ResponseModelStockMarketInvestment(**stock)
    
    stocks = list(map(validate, res.json()))
    print(stocks[0])

    assert res.status_code == 200
    assert len(res.json()) == len(test_stock_investment)
    
    assert stocks[0].id == test_stock_investment[0][0].id

def test_unauthorized_user_get_all_stock_investments(client, test_stock_investment):
    res = client.get("/stockinvestments/stock_market")

    assert res.status_code == 401

def test_unauthorized_user_get_one_stock_investment(client, test_stock_investment):
    res = client.get(f"/stockinvestments/{test_stock_investment[0][0].id}")

    assert res.status_code == 401

def test_get_one_stock_not_exist(authorized_client, test_stock_investment):
    res = authorized_client.get("/stockinvestments/99999999999")
    assert res.status_code == 404

def test_get_one_stock_investment(authorized_client, test_stock_investment):
    res = authorized_client.get(f"/stockinvestments/{test_stock_investment[0][0].id}")
    stock = schemas.ResponseModelStockMarketInvestment(**res.json())
    
    assert stock.id == test_stock_investment[0][0].id
    assert stock.income_type == test_stock_investment[0][1].income_type.value
    assert stock.type == test_stock_investment[0][1].type.value


@pytest.mark.parametrize("amount, income_type, type, ticker, shares",
                         [
                             (22, 'VARIABLE', 'BURSATIL','AMZ',2),
                             (1, 'VARIABLE', 'BURSATIL','C',2),
                             (100, 'VARIABLE', 'BURSATIL','Alphabet',1),
                         ])
def test_create_stock_investment(authorized_client, test_user, test_stock_investment, amount, income_type, type, ticker, shares):
    res = authorized_client.post("/stockinvestments/", json={"amount":amount ,"income_type":income_type,"type":type, "ticker":ticker, "shares":shares})
    new_stock = schemas.ResponseModelStockMarketInvestment(**res.json())
    assert res.status_code == 201
    assert new_stock.ticker == ticker


def test_unauthorized_user_create_stock_investments(client, test_stock_investment):
    res = client.post("/stockinvestments/", json={"amount":10 ,"income_type":"VARIABLE","type":"BURSATIL", "ticker":"GO", "shares":5})

    assert res.status_code == 401