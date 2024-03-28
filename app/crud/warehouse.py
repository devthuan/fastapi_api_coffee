from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from app.models.entities import generate_response
from app.schemas.order import OrderCreate
from sqlalchemy.orm import Session, load_only, Load
from sqlalchemy.exc import IntegrityError

from app.schemas.warehouse import WarehouseCreate
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




def restock_ingredient_crud(ingredient_for_product: list[WarehouseCreate], db: Session):
    try:
        for item_product in ingredient_for_product:
            
            product = db.query(tables.Products).filter(tables.Products.id == item_product.product_id).first()
            product.quantity_available += item_product.quantity_available
            
             # Lấy danh sách các công thức cho sản phẩm từ cơ sở dữ liệu
            formulas = db.query(tables.Formulas).filter(tables.Formulas.product_id == item_product.product_id).all()
            
            for item_formulas in formulas:
               
                # Lấy id của kho chứa nguyên liệu từ công thức
                warehouse_id = item_formulas.warehouse_id
                
                 # Tính toán số lượng mới của nguyên liệu dựa trên công thức và số lượng sản phẩm
                quantity_per_unit_new = item_formulas.quantity_required * item_product.quantity_available                
                
                # Lấy thông tin nguyên liệu trong kho từ cơ sở dữ liệu
                ingredient_in_warehouse = db.query(tables.Warehouse).filter(tables.Warehouse.id == warehouse_id).first()
                
                 # Cập nhật số lượng nguyên liệu trong kho
                ingredient_in_warehouse.quantity_per_unit += quantity_per_unit_new
                
        db.commit()
             
    except Exception as e:
      print(e)
      db.rollback()