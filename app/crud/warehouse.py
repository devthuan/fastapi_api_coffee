from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from app.models.entities import generate_response
from app.schemas.order import OrderCreate
from sqlalchemy.orm import Session, load_only, Load
from sqlalchemy.exc import IntegrityError

from app.schemas.warehouse import WarehouseUpdate, WarehouseCreate
from ..models import tables


def get_all_warehouses(user_id: int, db: Session):
    try:
        result = db.query(tables.Warehouse).all();
        
        if(result):
            return generate_response("success", 200, "get warehouse successfully", result)
        else:
            raise generate_response("error", 404, "Orders not found.")
        
    except Exception as e:
            raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))


def warehouse_import(warehouse: WarehouseCreate, db : Session):
    try:
        for item in warehouse.detail_ingredient:
            warehouse_model = tables.Warehouse (
                ingredient_name = item.ingredient_name,
                quantity_per_unit = item.quantity_per_unit,
                unit_of_measure = item.unit_of_measure,
                purchase_price = item.purchase_price,
                supplier_id = warehouse.supplier_id,
            )
            db.add(warehouse_model)
            db.commit()
        return generate_response("success", 200, "Create warehouse successfully")
            
    except RequestValidationError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e.errors())
    except IntegrityError  as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Warehouse creation failed. Please check foreign key constraints.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        

def update_warehouses_crud(warehouse_update: WarehouseUpdate, warehouse_id : int, db: Session):
    try:
        warehouse = db.query(tables.Warehouse).filter(tables.Warehouse.id == warehouse_id).first()
        if warehouse:
            warehouse.ingredient_name = warehouse_update.ingredient_name
            warehouse.quantity_per_unit = warehouse_update.quantity_per_unit
            warehouse.unit_of_measure = warehouse_update.unit_of_measure
            warehouse.purchase_price = warehouse_update.purchase_price
            warehouse.supplier_id = warehouse_update.supplier_id
            db.commit()
            return generate_response("success", 200, "update warehouse successfully", {warehouse})
        else:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "Warehouse not found"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
def delete_warehouses_crud(warehouse_id: int, db: Session):
    try:
        result = db.query(tables.Warehouse).filter(tables.Warehouse.id == warehouse_id).first()
        if result:
            db.delete(result)
            db.commit()
            return generate_response("success", 200, "deleted warehouse successfully", {result})
        else :
            raise generate_response("error", 404, "Warehouse not found.")
               
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")