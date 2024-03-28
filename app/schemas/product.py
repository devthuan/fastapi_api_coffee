from datetime import datetime
from typing import List, Optional, Union
from fastapi import File, UploadFile
from pydantic import BaseModel, Field, validator
from sqlalchemy import Boolean

from app.schemas.formulas import FormulasCreate

class CreateProduct(BaseModel):
    name: str
    image: str
    category_id: int
    price: float
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Price must be greater than 0.")
        return v
class UpdateProduct(BaseModel):
    name: str
    image: str
    category_id: int
    price: float
    is_active: bool
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Price must be greater than 0.")
        return v
    
class UpdateProductDetail(BaseModel):
    name: str
    price: float
    image: str
    category_id: int
    



