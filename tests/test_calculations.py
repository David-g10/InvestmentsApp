import pytest
from app.calculations import add, substract, multiply, divide, BankAccount, InsufficientFunds

# Fixture are like dependencies, functions that be executed
# before the test that uses them.
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

# parametrize is helpfull to test a lot of samples at same time.
@pytest.mark.parametrize("num1, num2, expected_value", [
    (3,2,5), (1,1,2), (12,17,29)
])
def test_add(num1, num2, expected_value):
    print("testing func")
    assert add(num1, num2) == expected_value

def test_substract():
    assert substract(9,4) == 5

def test_multiply():
    assert multiply(4,4) == 16

def test_divide():
    assert divide(10,5) == 2




def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_bank_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 55   


@pytest.mark.parametrize("deposited, withdrew, expected_amount", [
    (200,50,150), (10,5,5), (1200,200,1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected_amount):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected_amount


def test_insufficient_funds(bank_account):
    # This is the way to tell python that the test is waiting
    # for an exception.
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
    

