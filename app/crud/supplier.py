from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from app.models.entities import generate_response
from app.schemas.order import OrderCreate
from sqlalchemy.orm import Session, load_only, Load
from sqlalchemy.exc import IntegrityError

from app.schemas.supplier import SupplierCreate
from ..models import tables



def create_supplier_crud(supplier: SupplierCreate, db : Session):
    supplier_model = tables.Suppliers(
            name_supplier= supplier.name_supplier,
            address = supplier.address ,
            phone = supplier.phone ,
            email = supplier.email  
    )
    try:
        db.add(supplier_model)
        db.commit()
        db.refresh(supplier_model)
        return generate_response("success", 200, "Create supplier successfully", {supplier_model})
            
    except RequestValidationError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e.errors())
    except IntegrityError  as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="supplier creation failed. Please check foreign key constraints.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_all_suppliers_crud(user_id: int, db: Session):
    try:
        result = db.query(tables.Suppliers).all();
        
        if(result):
            return generate_response("success", 200, "get all supplier successfully", result)
        else:
            raise generate_response("error", 404, "supplier not found.")
        
    except Exception as e:
            raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))
    

def update_supplier_crud(supplier_update: SupplierCreate, suppluer_id : int, db: Session):
    try:
        result_query = db.query(tables.Suppliers).filter(tables.Suppliers.id == suppluer_id).first()
        if result_query:
            result_query.name_supplier = supplier_update.name_supplier
            result_query.address = supplier_update.address
            result_query.phone = supplier_update.phone
            result_query.email = supplier_update.email
            db.commit()
            return generate_response("success", 200, "update supplier successfully", {result_query})
        else:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "supplier not found"))
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
def delete_supplier_crud(supplier_id: int, db: Session):
    try:
        result = db.query(tables.Suppliers).filter(tables.Suppliers.id == supplier_id).first()
        if result:
            db.delete(result)
            db.commit()
            return generate_response("success", 200, "deleted supplier successfully", {result})
        else :
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "supplier not found"))
            
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")