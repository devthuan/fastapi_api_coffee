from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.cart import CartBase
from ..schemas.users import AuthUser, EditUser, UserBase


from ..database import  SessionLocal
from ..crud import user, cart
from ..models.entities import ResponseStatus, generate_response
from ..services.authenticate import get_current_user_id, has_permission, validate_token

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router_cart = APIRouter()


@router_cart.post("/cart")
def add_product_to_cart(new_cart: CartBase,user_id : int = Depends(get_current_user_id), db : Session = Depends(get_db)):
    return cart.create_cart(new_cart, user_id, db)

@router_cart.get("/cart")
def get_cart_by_user(user_id: int  =  Depends(get_current_user_id), db : Session = Depends(get_db)):
    return cart.get_cart_by_user_id(user_id, db)

@router_cart.get("/carts")
def get_cart_by_user(page: int = Query(1), limit: int = Query(10), db : Session = Depends(get_db)):
    return cart.get_all_cart(page, limit, db)

@router_cart.patch("/cart/{cart_id}")
def update_quantity_cart(quantity : int, cart_id,  db :Session = Depends(get_db)):
    try:
        if quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity is not less than 0")
        return cart.update_quantity(cart_id, quantity, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e

@router_cart.delete("/cart/{cart_id}")
def delete_item_cart(cart_id, user_id : int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        return cart.remove_item_cart_by_cartID(cart_id, user_id, db)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    
@router_cart.delete("/cart-all")
def delete_item_cart_by_user(user_id : int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        return cart.remove_item_cart_by_userId(user_id, db)
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    

fake_items = [{"item_id": str(i)} for i in range(1, 101)]  # Dữ liệu giả

@router_cart.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items[skip : skip + limit]