from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..schemas.users import AuthUser, EditUser, UserBase


from ..database import  SessionLocal
from ..crud import user
from ..models.entities import ResponseStatus, generate_response
from ..services.authenticate import has_permission, validate_token

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router_user = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router_user.get("/users")
def get_all_user(page: int = Query(1, gt=0), limit: int = Query(10, gt=0),db:Session = Depends(get_db), current_user: AuthUser = Depends(validate_token) ):
    try:
        role_id, list_permission = current_user
        if not has_permission(list_permission, "READ_USERS"):
            return generate_response("error", status.HTTP_401_UNAUTHORIZED, "You do not have access !")
        
        list_user =  user.get_all_user(page, limit, db)
        return generate_response("success", status.HTTP_200_OK, "get all user success", list_user)
    except HTTPException as e:
        if e.status_code == 401:
            return generate_response("error", status.HTTP_401_UNAUTHORIZED, "Invalid token")
    except Exception as e:
        return generate_response("error", status.HTTP_500_INTERNAL_SERVER_ERROR, e)
   

@router_user.get("/user/{user_id}")
def get_user_by_id(user_id, db: Session = Depends(get_db)):
    try:
        return  user.get_user_by_id(db, user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
      return generate_response("error", status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error.",e)

@router_user.post("/user")
def create_user_route(user_form: UserBase, db: Session = Depends(get_db)):
    try:
        new_user = user.new_user(user_form, db)
        return new_user
    except HTTPException as e:
        # Xử lý các HTTPException tại đây (nếu cần)
        raise e
    except Exception as e:
        # Xử lý các lỗi khác tại đây
        raise HTTPException(status_code=500, detail="Internal server error")

@router_user.patch("/user/{user_id}")
def update_user(new_user: EditUser, user_id, db: Session = Depends(get_db)):
    try:
        return user.update_user(new_user,user_id, db)
    except HTTPException as e:
        # Xử lý các HTTPException tại đây (nếu cần)
        raise e
    except Exception as e:
        # Xử lý các lỗi khác tại đây
        raise HTTPException(status_code=500, detail="Internal server error")

@router_user.patch("/user/active/{user_id}")
def change_status_user(user_id, db : Session = Depends(get_db)):
    return user.change_active_user(user_id,db)
