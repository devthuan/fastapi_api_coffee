from fastapi import status
from datetime import datetime
from enum import Enum
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import func, text
from sqlalchemy.orm import Session


from ..schemas.users import ChangePassBase, UserCreate, UserBase
from .user import get_user_by_email, get_user_by_id, get_user_full_by_id
from ..services import authenticate
from ..models.tables import User, Role, RolePermission, Permission
from ..models.entities import ResponseStatus, generate_response


# def login(user: UserCreate, db: Session):
#     try:
#         result = get_user_by_email(db, user.email)
#         if status_custom == ResponseStatus.NOT_FOUND:
#             return None, ResponseStatus.NOT_FOUND

#         check_pass = authenticate.verify_password(user.password, info_user.password)
#         if not check_pass:
#             return None, ResponseStatus.UNAUTHORIZED

#         return info_user, None
#     except ValidationError as e:
#         return e, ResponseStatus.VALIDATION_ERROR
#     except Exception as e:
#         return e, ResponseStatus.INTERNAL_SERVER_ERROR
  
    
def login(user_login: UserCreate, db: Session):
    try:
        user = get_user_by_email(db, user_login.email)
        hashed_pass = user.get("data").get("password")
        info_user = user.get("data")
        check_pass = authenticate.verify_password(user_login.password, hashed_pass)
        
        if not check_pass:
            raise HTTPException(status_code=401, detail=generate_response("error",401, "Email or password incorrect"))

        list_permission = get_user_permission(db, info_user.get("id"))
        token = authenticate.create_access_token({"id": info_user.get("id"), "email": info_user.get("email"), "role": info_user.get("role"), "list_permission": list_permission})
        return generate_response("success",200, "Login successful", {"access_token": token})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
  
    
    


def get_user_permission(db: Session, user_id: int):
      try:
        list_permission = db.query(User)\
          .filter(User.id == user_id)\
          .join(Role)\
          .join(RolePermission, RolePermission.role_id == Role.id)\
          .join(Permission, RolePermission.permission_id == Permission.id)\
          .with_entities(Permission.code)\
          .all()
          # convert object type row to dict
        list_permission = [permission[0] for permission in list_permission]
        return list_permission
      
      except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve user permissions")

def change_password_CRUD(form_pass: ChangePassBase,user_id: int, db: Session):
  try:
    # return form_pass, user_id
    info_user = get_user_full_by_id(db, user_id)
    check_pass = authenticate.verify_password(form_pass.current_pass, info_user.get("data").get("password"))
    if check_pass is False:
      raise HTTPException(status_code=401, detail=generate_response("error",401, "Email or password incorrect"))

    # hashing password
    new_hash_pass = authenticate.get_password_hash(form_pass.new_pass)
    
    # update database
    query = text("UPDATE users SET password=:new_hash_pass WHERE id=:user_id")
    result = db.execute(query, {"new_hash_pass": new_hash_pass, "user_id": user_id})
    rows_affected = result.rowcount
    if rows_affected > 0:
            db.commit()
            return generate_response("success", 200, "Password changed successfully.")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=generate_response("error", 500, "Failed to update password"))
  except HTTPException as e:
      raise e
  except Exception as e:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=generate_response("error", 500, "Internal server error."))
  