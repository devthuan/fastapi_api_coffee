from datetime import datetime
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import func, text
from sqlalchemy.orm import Session, load_only, Load
from sqlalchemy.exc import IntegrityError, InvalidRequestError, OperationalError, ProgrammingError, SQLAlchemyError


from ..schemas.users import EditUser, UserBase, UserLogin
from ..services import authenticate

from ..models import tables
from ..models.entities import ResponseStatus, generate_response



def get_user_by_id(db: Session, user_id: int):
    user = db.query(tables.User).filter(tables.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail=generate_response("error", 404, "User not found"))
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail=generate_response("error", 401, "Your user is not activated or locked"))
    
    user_data = {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "role_id": user.role_id,
        "created_date": user.created_date
    }
    return generate_response("success", 200, "get user success", user_data)  

def get_user_by_word_email(search: str, db: Session):
    try:
        user_role = db.query(tables.User, tables.Role)\
                      .join(tables.Role, tables.User.role_id == tables.Role.id)\
                      .filter(tables.User.email.like(f"{search}%"))\
                      .all()
        
        if not user_role:
            return generate_response("success", 200, "No users found", [])

        data_res = [
            {
            "id": user.id,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "role_code": role.code,
            "role_name": role.name,
            "role_description": role.description,   
            "role_id": user.role_id,
            "is_active": user.is_active,
            "created_date": user.created_date
        } for user, role in user_role
        ]
        
        return generate_response("success", 200, "get user success", data_res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def get_user_full_by_id(db: Session, user_id: int):
    user = db.query(tables.User).filter(tables.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail=generate_response("error", 404, "User not found"))
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail=generate_response("error", 401, "Your user is not activated or locked"))
    
    user_data = {
        "id": user.id,
        "email": user.email,
        "password": user.password,
        "is_active": user.is_active,
        "role_id": user.role_id,
        "created_date": user.created_date
    }
    return generate_response("success", 200, "get user success", user_data)  


def get_user_by_email(db: Session, email: str):
    user = db.query(tables.User).filter(tables.User.email == email)\
            .join(tables.Role, tables.User.role_id == tables.Role.id)\
            .first()
    
    if not user:
        raise HTTPException(status_code=404, detail=generate_response("error", 404, "User not found"))
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail=generate_response("error", 401, "Your user is not activated or locked"))
    
    user_data = {
        "id": user.id,
        "email": user.email,
        "password": user.password,
        "is_active": user.is_active,
        "role": user.role.code,
        "created_date": user.created_date
    }
    
    
    return generate_response("success", 200, "get user success", user_data)  
   

def get_all_user(page: int, limit:int, db: Session):
    offset = (page -1) * limit
    try:
        users = db.query(tables.User, tables.Role)\
                    .join(tables.Role, tables.User.role_id == tables.Role.id)\
                    .offset(offset)\
                    .limit(limit).all()
        total_items = db.query(tables.User).count()
        total_pages = (total_items + limit - 1 ) // limit
        if not users:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "User not found"))
        serialized_users = [
            {
                "id": user.id,
                "email": user.email,
                "phone": user.phone,
                "address": user.address,
                "role_code": role.code,
                "role_name": role.name,
                "role_description": role.description,   
                "role_id": user.role_id,
                "is_active": user.is_active,
                "created_date": user.created_date
            }
            for user, role in users
        ]
        data_res = {
            "page": page,
            "total_page": total_pages,
            "limit": limit,
            "total_items": total_items,
            "data": serialized_users,
            
        }
        return generate_response("success", 200, "get user success", data_res)
    except SQLAlchemyError as e:
        # Xử lý các lỗi từ cơ sở dữ liệu
        db.rollback()
        raise HTTPException(status_code=500, detail=generate_response("error", 500, "Database error"))
    except Exception as e:
        # Xử lý các lỗi khác
        raise HTTPException(status_code=500, detail=generate_response("error", 500, "Internal server error"))
    
    
  
def new_user(user: UserBase, db: Session):
    try:
        hashing_password = authenticate.get_password_hash(user.password)
        new_user = tables.User(
            email= user.email,
            password= hashing_password,
            role_id= user.role_id,
            is_active=user.is_active
        )
        db.add(new_user)
        db.commit()
        return generate_response("success", 200,"Create account successfully.")
    # bắt lỗi unique
    except IntegrityError as e: 
        print(e)
        db.rollback()
        raise HTTPException(status_code=400, detail=generate_response("error", 400,"Email already exists."))
    # các lỗi khác
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=generate_response("error", 500,"Internal server error."))
    
def update_user(user_update: EditUser, user_id: int, db: Session):
    try:
        user = db.query(tables.User).filter(tables.User.id == user_id).first();
        
        if user:
             # Cập nhật các thuộc tính của đối tượng người dùng
            for key, value in user_update.dict().items():
                setattr(user, key, value)
  
            db.commit()
            return generate_response("success", 200,"Update user successfully.")
        else:
            raise HTTPException(status_code=404, detail=generate_response("error", 404,"User not found."))

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=generate_response("error", 500,"Internal server error.", str(e)))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=generate_response("error", 500,"Internal server error.", str(e)))
    
def change_active_user(user_id: int, db: Session):
    pass
    try:
        user = db.query(tables.User).filter(tables.User.id == user_id).first()
        if user:
            user.is_active = not user.is_active
            db.commit()
            return generate_response("success", 200, "Change active user successfully.")
        else:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "User not found."))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=generate_response("error", 500,"Internal server error."))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=generate_response("error", 500,"Internal server error."))
