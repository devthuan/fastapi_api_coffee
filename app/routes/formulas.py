


from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..schemas.order import OrderBase,OrderCreate, OrderDetailBase


from ..database import  SessionLocal
from ..crud import formulas
from ..models.entities import ResponseStatus, generate_response
from ..services.authenticate import get_current_user_id, has_permission, validate_token

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router_formulas = APIRouter()


@router_formulas.get("/formulas")
def get_all_formulas(db: Session = Depends(get_db)):
    return formulas.get_all_formulas_crud(db)