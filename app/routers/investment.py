from app import schemas
from fastapi import status, HTTPException, Response, APIRouter
from ..config import database
from typing import List

router = APIRouter(
    prefix="/investments",
    tags=["Investments"]
)

conn, cursor = database.Database().connect()

@router.get("/", response_model=List[schemas.ResponseModelInvestment])
def get_investments():
    cursor.execute("SELECT * FROM investments")
    investments = cursor.fetchall()
    return investments

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseModelInvestment)
def add_investment(investment: schemas.CreateInvestment):
    cursor.execute("""INSERT INTO investments (investment_name, token, amount) VALUES (%s, %s, %s) RETURNING * """,
                  (investment.investment_name, investment.token, investment.amount))
    new_investment = cursor.fetchone()
    conn.commit()

    return new_investment

@router.get("/{id}", response_model=schemas.ResponseModelInvestment)
def get_investment(id: int):
    cursor.execute("""SELECT * FROM investments WHERE id = %s""", (str(id)))
    investment = cursor.fetchone()
    if not investment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"investment with id: {id} was not found.")
    return investment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_investment(id: int):
    
    cursor.execute("""DELETE FROM investments WHERE id = %s RETURNING *""", (str(id)))
    deleted_investment = cursor.fetchone()
    conn.commit()

    if deleted_investment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'investment with id {id} does not exist.')

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ResponseModelInvestment)
def update_investment(id: int, investment: schemas.UpdateInvestment):
    
    cursor.execute("""UPDATE investments SET amount=%s WHERE id=%s RETURNING *""",
     (investment.amount, str(id)))
    updated_investment = cursor.fetchone()
    conn.commit()
    if updated_investment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'investment with id {id} does not exist.')
    
    return updated_investment