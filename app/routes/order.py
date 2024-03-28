


from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..schemas.order import OrderBase,OrderCreate, OrderDetailBase


from ..database import  SessionLocal
from ..crud import order
from ..models.entities import ResponseStatus, generate_response
from ..services.authenticate import get_current_user_id, has_permission, validate_token

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router_order = APIRouter()



@router_order.post("/order")
def create_order( new_order: OrderCreate, user_id: int = Depends(get_current_user_id), db : Session = Depends(get_db)):
    return order.create_order_crud(new_order, user_id, db)


@router_order.get("/order")
def get_order_by_user_id(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return order.get_order_by_user(user_id, db);


@router_order.get("/order-all")
def get_order_by_user_id( page: int = Query(1), limit: int = Query(20), db: Session = Depends(get_db)):
    return order.get_all_order(page, limit, db);


@router_order.patch("/order-status/{order_id}")
def update_status_order(order_id, new_status: str, db: Session = Depends(get_db)):
    return order.update_status_order_crud(order_id, new_status, db)