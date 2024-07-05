from app import schemas
from fastapi import status, HTTPException, Response, APIRouter, Depends, Query
from typing import List, Optional
from .. import oauth2
from ..config import orm_models, orm_database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/investments",
    tags=["Investments"]
)

@router.get("/", response_model=List[schemas.ResponseModelInvestment])
def get_investments(
    db: Session = Depends(orm_database.get_db),  # Dependencia para obtener la sesión de la base de datos
    current_user: int = Depends(oauth2.get_current_user),
    search_filter: Optional[str] = Query(None, alias="investment_token")
):
    query = db.query(orm_models.Investment)  # Utiliza el modelo ORM para construir la consulta
    query = query.filter(orm_models.Investment.user_id == current_user["id"])  # Filtra por el usuario actual

    if search_filter:
        query = query.filter(orm_models.Investment.token == search_filter)  # Aplica filtro adicional si es necesario

    investments = query.all()  # Ejecuta la consulta y recupera todos los resultados

    return investments

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseModelInvestment)
def add_investment(
    investment: schemas.CreateInvestment,
    db: Session = Depends(orm_database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # Crear el objeto del modelo ORM
    new_investment = orm_models.Investment(
        user_id=current_user["id"],
        investment_name=investment.investment_name,
        token=investment.token,
        amount=investment.amount,
    )
    # new_investment = orm_models.Investment(**investment.dict())
    # Agregar el objeto a la sesión
    db.add(new_investment)
    
    # Intentar hacer commit de los cambios
    try:
        db.commit()
    except Exception as e:
        db.rollback()  # Si hay un error, hacer rollback
        raise HTTPException(status_code=400, detail=f"Error al guardar en la base de datos: {str(e)}")
    
    # Refrescar el objeto para asegurar que contiene cualquier actualización de la base de datos
    db.refresh(new_investment)
    
    # Devolver el objeto recién creado y guardado
    return new_investment

@router.get("/{id}", response_model=schemas.ResponseModelInvestment)
def get_investment(
    id: int, 
    db: Session = Depends(orm_database.get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    # Buscar la inversión por ID usando el ORM
    investment = db.query(orm_models.Investment).filter(orm_models.Investment.id == id).first()

    # Verificar si la inversión existe
    if not investment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Investment with id: {id} was not found.")

    # Verificar si el usuario actual tiene permiso para ver esta inversión
    if current_user["id"] != investment.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action.")

    # Si todo está bien, retornar la inversión
    return investment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_investment(
    id: int,
    db: Session = Depends(orm_database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # Buscar la inversión por ID
    investment = db.query(orm_models.Investment).filter(orm_models.Investment.id == id).first()

    if not investment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Investment with id {id} does not exist.")

    if current_user["id"] != investment.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    # Eliminar la inversión si todo está correcto
    db.delete(investment)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ResponseModelInvestment)
def update_investment(
    id: int,
    investment_data: schemas.UpdateInvestment,
    db: Session = Depends(orm_database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    # Buscar la inversión por ID
    investment = db.query(orm_models.Investment).filter(orm_models.Investment.id == id).first()

    if not investment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Investment with id {id} does not exist.")

    if current_user["id"] != investment.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")

    # Actualizar los campos necesarios
    if investment_data.amount is not None:
        investment.amount = investment_data.amount

    db.commit()
    db.refresh(investment)

    return investment