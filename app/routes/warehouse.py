


from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.warehouse import WarehouseCreate

from ..schemas.order import OrderBase,OrderCreate, OrderDetailBase


from ..database import  SessionLocal
from ..crud import warehouse
from ..models.entities import ResponseStatus, generate_response
from ..services.authenticate import get_current_user_id, has_permission, validate_token

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router_warehouse = APIRouter()



@router_warehouse.get("/warehouses")
def create_ingredient(user_id : int = Depends(get_current_user_id),  db : Session = Depends(get_db)):
    return warehouse.get_all_warehouses(user_id,db)


@router_warehouse.post("/restock")
def create_ingredient( ingredient_for_product: list[WarehouseCreate],  db : Session = Depends(get_db)):
    return warehouse.restock_ingredient_crud(ingredient_for_product,db)


