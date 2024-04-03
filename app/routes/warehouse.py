


from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.warehouse import  WarehouseCreate, WarehouseUpdate



from ..database import  SessionLocal
from ..crud import warehouse
from ..crud.warehouse import warehouse_import
from ..services.authenticate import get_current_user_id, has_permission, validate_token

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router_warehouse = APIRouter()




@router_warehouse.post("/warehouses")
def create_warehouses(warehouse: WarehouseCreate, db : Session = Depends(get_db)):
    return warehouse_import(warehouse, db)


@router_warehouse.get("/warehouses")
def get_all_warehouse(user_id : int = Depends(get_current_user_id),  db : Session = Depends(get_db)):
    return warehouse.get_all_warehouses(user_id,db)


@router_warehouse.put("/warehouses/{warehouse_id}")
def update_warehouses(warehouse_id: int, update_warehouse: WarehouseUpdate,  db : Session = Depends(get_db)):
    # return update_warehouse
    return warehouse.update_warehouses_crud(update_warehouse, warehouse_id,db)

@router_warehouse.delete("/warehouses/{warehouse_id}")
def delete_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    return warehouse.delete_warehouses_crud(warehouse_id, db)