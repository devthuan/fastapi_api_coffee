
from datetime import timedelta, timezone, datetime
import os
from typing import Union
from dotenv import load_dotenv

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jwt import DecodeError, ExpiredSignatureError
import jwt

from ..schemas.users import AuthUser

load_dotenv()

# Khóa bí mật để mã hóa và giải mã token
SECRET_KEY = os.getenv("SECRET_KEY")
# Thời gian hết hạn của token (ví dụ: 15 phút)
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # Raised when the hashed password has an invalid format
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid hashed password format")
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to verify password")

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("EXPIRE_TOKEN")))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise HTTPException(status_code=401)
        role_id = payload.get("role_id")
        list_permission = payload.get("list_permission")
        return role_id, list_permission
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except DecodeError:
      raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      if not payload:
          raise HTTPException(status_code=401, detail="")
      user_id = payload.get("id")
      return user_id
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except DecodeError:
      raise HTTPException(status_code=401, detail="Invalid token")

# # Custom decorator for role-based authorization
# def check_role(allowed_roles: list[str] = []):
#     async def inner(func):
#         async def wrapper(token: str = Depends(oauth2_scheme)):
#             # Extract user role from authentication context (replace with your logic)
#             user_role = validate_token(token)
#             if user_role not in allowed_roles:
#                 raise HTTPException(status_code=403, detail="Forbidden")
#             return await func(token)
#         return wrapper
#     return inner

def has_permission(user_role, required_permission):
    if required_permission in user_role:
        return True
    return False