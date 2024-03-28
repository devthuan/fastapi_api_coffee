from datetime import datetime
from typing import List
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy import func, text, update, and_
from sqlalchemy.orm import Session, load_only, Load
from sqlalchemy.exc import IntegrityError, InvalidRequestError, OperationalError, ProgrammingError, SQLAlchemyError

from app.schemas.cart import CartBase


from ..schemas.users import UserBase, UserLogin
from ..schemas.product import CreateProduct
from ..services import authenticate

from ..models import tables
from ..models.entities import ResponseStatus, generate_response

def create_cart(new_cart: CartBase, user_id: int, db: Session):
    cart = tables.Cart(
        user_id = user_id,
        product_id = new_cart.product_id,
        quantity = new_cart.quantity,
    )        
    try:
        cart_exist = db.query(tables.Cart).filter(and_(tables.Cart.product_id == new_cart.product_id, tables.Cart.user_id == user_id)).first()
        if(cart_exist is not None):
            print(cart_exist.quantity)
            cart_exist.quantity +=1
            db.add(cart_exist)
            db.commit()
            db.refresh(cart_exist)
            return generate_response("success", 200, "add product to add successfully.", cart_exist)
        else:
            db.add(cart)
            db.commit()
            db.refresh(cart)
            return generate_response("success", 200, "add product to add successfully.", cart)
        
    
    except RequestValidationError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=generate_response("error", 500, "Internal server error.", str(e)))
    except IntegrityError  as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=generate_response("error", 500, "Cart creation failed. Please check foreign key constraints.", str(e)))
    except Exception as e:
      raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))


def get_cart_by_user_id(user_id: int, db: Session):
    try:
        query = text("SELECT cart.id, product_id, name_product, price, quantity, image_product, cart.created_date  FROM cart JOIN products on cart.product_id = products.id WHERE user_id=:user_id")
        result = db.execute(query, {"user_id": user_id})
        rows = result.fetchall()
        cart_data = [{"cart_id": row[0],
                      "product_id": row[1],
                      "name_product": row[2], 
                      "price": row[3],
                      "quantity": row[4],
                       "image_product": row[5],
                       "created_date": row[6]
                       } for row in rows]
        return generate_response("success", 200, "get all cart successfully.", cart_data)
        
                    
    except Exception as e:
        raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))

def get_all_cart(page:int, limit: int, db:Session):
    offset = (page -1) * limit
    try:
        query = text("SELECT cart.id, name_product, price, quantity, image_product, cart.created_date  FROM cart JOIN products on cart.product_id = products.id LIMIT :limit OFFSET :offset ")
        result = db.execute(query, {"limit": limit, "offset": offset})
        rows = result.fetchall()
        total_items = db.query(tables.Cart).count()
        total_pages = (total_items + limit -1) // limit
        cart_data = tuple({"cart_id": row[0],
                        "name_product": row[1], 
                        "price": row[2],
                        "quantity": row[3],
                        "image_product": row[4],
                        "created_date": row[5]
                        } for row in rows)
        data_res = {
            "page": page,
            "total_page": total_pages,
            "limit": limit,
            "data": cart_data,
            
        }
        return generate_response("success", 200, "get all cart successfully.", data_res)  
    except Exception as e:
        raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))
    

def update_quantity(cart_id: int, quantity: int, db : Session):
    try:
        cart = db.query(tables.Cart).filter(tables.Cart.id == cart_id).first()
        if cart:
            cart.quantity = quantity
            db.commit()
            return generate_response("success", 200, "update quantity successful.")  
        else:  
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "Cart not found."))
            
    except Exception as e:
        raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))
    
def remove_item_cart_by_cartID(cart_id: int, user_id: int, db : Session):
    try:
        cart_item = db.query(tables.Cart).filter(tables.Cart.id == cart_id and tables.user_id ==  user_id).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "Item not found in cart."))
        
        db.delete(cart_item)
        db.commit()
        
        return generate_response("success", 200, "Item removed successfully.")  
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))
    
def remove_item_cart_by_userId( user_id: int, db : Session):
    try:
        cart_items = db.query(tables.Cart).filter(tables.Orders.user_id ==  user_id).all()
        
        if not cart_items:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "Item not found in cart."))
        
        # Xóa tất cả các hàng tìm thấy
        for cart_item in cart_items:
            db.delete(cart_item)
            
        db.commit()
        
        return generate_response("success", 200, "Item removed successfully.")  
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))