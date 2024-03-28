from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from app.models.entities import generate_response
from app.schemas.order import OrderCreate
from sqlalchemy.orm import Session, load_only, Load
from sqlalchemy.exc import IntegrityError

from app.schemas.warehouse import WarehouseCreate
from ..models import tables



def get_all_formulas_crud( db: Session):
    try:
        data_res = []
        # Sử dụng join để lấy thông tin từ các bảng liên quan
        formulas_query = db.query(tables.Formulas, tables.Products, tables.Warehouse)\
            .join(tables.Products, tables.Formulas.product_id == tables.Products.id)\
            .join(tables.Warehouse, tables.Formulas.warehouse_id == tables.Warehouse.id)\
            .group_by(tables.Formulas.id)\
            .all()

        if formulas_query:
            for formulas, products, warehouses in formulas_query:
                data_res.append({
                    "id": formulas.id,
                    "name_product": products.name_product,
                    "price": products.price,
                    "image_product": products.image_product,
                    "warehouse_id": warehouses.id,
                    "ingredient_name": warehouses.ingredient_name,
                    "quantity_required": formulas.quantity_required,
                    "unit_of_measure": warehouses.unit_of_measure
                })
            return generate_response("success", 200, "get warehouse successfully", data_res)
        else:
            raise generate_response("error", 404, "Orders not found.")
        
    except Exception as e:
            raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))

