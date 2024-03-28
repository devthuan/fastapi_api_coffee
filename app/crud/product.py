from datetime import datetime
from typing import List
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy import func, text, update
from sqlalchemy.orm import Session, load_only, Load
from sqlalchemy.exc import IntegrityError, InvalidRequestError, OperationalError, ProgrammingError, SQLAlchemyError


from ..schemas.users import UserBase, UserLogin
from ..schemas.product import CreateProduct, UpdateProductDetail
from ..services import authenticate

from ..models import tables
from ..models.entities import ResponseStatus, generate_response


def create_product(new_product: CreateProduct, db: Session):
    product_model = tables.Products(
        name_product = new_product.name,
        image_product = new_product.image,
        category_id = new_product.category_id,
        price = new_product.price,
        quantity_available = 0,
        is_active = 1
    
    )
    try:
        
        db.add(product_model)
        db.commit()
        db.refresh(product_model)
        
        return generate_response("success", 200, "Create product successfully", product_model)
    
    except RequestValidationError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e.errors())
    except IntegrityError  as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Product creation failed. Please check foreign key constraints.")
    except Exception as e:
        db.rollback()
        raise e

# def insert_multi_products(products: List[CreateProduct], db: Session) -> List[CreateProduct]:
#     product_models = []
#     for product in products:
#         product_model = tables.Products(
#             name_product=product.name,
#             image_product=product.image,
#             category_id=product.category_id,
#             price=product.price
#         )
#         db.add(product_model)
#         db.commit()
#         db.refresh(product_model)
#         product_models.append(product_model)
#     return product_models


def get_all_product(page:int , limit:int, db: Session):
    offset = (page - 1) * limit
    try:
        products = db.query(tables.Products)\
                    .join(tables.Category, tables.Products.category_id == tables.Category.id)\
                    .offset(offset)\
                    .limit(limit).all()
        if not products:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "Product not found"))
        data_product_detail =[]
        for product in products:
                      
            data_product_detail.append({
                "id": product.id,
                 "name_product": product.name_product,
                 "price": product.price,
                 "quantity_available": product.quantity,
                 "image_product": product.image_product,
                 "is_active": product.is_active,
                "category": product.category.name_category,
                "category_id": product.category_id,
                "created_date": product.created_date
                
                } )
            
        
        total_items = db.query(tables.Products).count()
        total_pages = (total_items + limit - 1 ) // limit
        data_res = {
            "page": page,
            "total_page": total_pages,
            "limit": limit,
            "data": data_product_detail,

            
        }
        return generate_response("success", 200, "Get all product successfully", data_res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        

def get_product_by_id(product_id: int, db:Session):
    try:
        product = db.query(tables.Products).filter(tables.Products.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "Product not found"))
        else:
            return generate_response("success", 200, "Get product successfully", product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_product_by_name(name_product: str, db:Session):
    try:
        products = db.query(tables.Products).filter(tables.Products.name_product.like(f"{name_product}%"))\
                    .join(tables.Category, tables.Products.category_id == tables.Category.id)\
                    .all()
        
        if not products:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "Product not found"))
        else:
            data_product_detail =[]
            for product in products:
                        
                data_product_detail.append({
                    "id": product.id,
                    "name_product": product.name_product,
                    "price": product.price,
                    "quantity_available": product.quantity,
                    "image_product": product.image_product,
                    "is_active": product.is_active,
                    "category": product.category.name_category,
                    "category_id": product.category_id,
                    "created_date": product.created_date
                    } )
            return generate_response("success", 200, "Get product successfully", data_product_detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



def update_product_CRUD(product: UpdateProductDetail,product_id : int, db: Session):
    try:
        result = db.execute(update(tables.Products)
                            .where(tables.Products.id == product_id)
                            .values(
                                name_product=product.name,
                                image_product=product.image,
                                category_id=product.category_id,
                                quantity=product.quantity,
                                price=product.price
                            ))
        
       
        rows_affected = result.rowcount
        # Kiểm tra có hàng nào được cập nhật không
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail=generate_response("error", 404,"Product not found."))

        
        # Commit thay đổi vào cơ sở dữ liệu
        db.commit()
        return generate_response("success", 200,"Update product successfully.")

    except RequestValidationError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=e.errors())
    except IntegrityError  as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Product creation failed. Please check foreign key constraints.")
    except Exception as e:
        db.rollback()
        print(e)
        raise e


def change_status_product(product_id:int, db:Session):
    try:
        product = db.query(tables.Products).filter(tables.Products.id == product_id).first()
        if product:
            product.is_active = not product.is_active
            db.commit()
            return generate_response("success", 200, "Change active product successfully.")
        else:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "Product not found."))
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=generate_response("error", 500,"Internal server error."))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=generate_response("error", 500,f"Internal server error: {str(e)}"))
    
 