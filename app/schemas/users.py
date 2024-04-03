from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, Field, constr
from sqlalchemy import Boolean

class UserCreate(BaseModel):
    email: str
    password: str
    

class UserBase(BaseModel):
    email: EmailStr
    password: constr(min_length=1)
    is_active: Optional[bool] = True
    role_id: Optional[int]
        
class UserLogin(BaseModel):
    email: str
    password: str
    status: str
    role_id: int

class EditUser(BaseModel):
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    role_id: int
    is_active: bool
    
class AuthUser(BaseModel):
    role: str
    list_permission: List[str]
    
class ChangePassBase(BaseModel):
    current_pass: str
    new_pass: constr(min_length=1)