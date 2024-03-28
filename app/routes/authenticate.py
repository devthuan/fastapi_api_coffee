from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session



from ..schemas.users import AuthUser, ChangePassBase, UserCreate
from ..services.authenticate import get_current_user_id, verify_password, create_access_token, validate_token
from ..crud import authenticate
from ..database import  SessionLocal
from ..crud.authenticate import ResponseStatus
from ..models.entities import generate_response
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router_authenticate = APIRouter()


@router_authenticate.post("/login")
async def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return authenticate.login(user, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")


@router_authenticate.post("/change_password")
async def ChangePassword(pass_form: ChangePassBase,user_id: Annotated[int, Depends(get_current_user_id)],  db: Session = Depends(get_db)):
    return authenticate.change_password_CRUD(pass_form, user_id,db)


@router_authenticate.post("/forgot_password")
def forgot_password(db:Session = Depends(get_db)):
    pass