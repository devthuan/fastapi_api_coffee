from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, Field, constr, validator
from sqlalchemy import Boolean


class WarehouseBase(BaseModel):
    id: int
    ingredient_name: str
    quantity_per_unit: float
    unit_of_measure: str
    purchase_price: float
    supplier_id: int
    
    @validator('quantity_per_unit')
    def price_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Price must be greater than 0.")
        return v
    
    @validator('purchase_price')
    def price_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Price must be greater than 0.")
        return v

class DetailIngredient(BaseModel):
    ingredient_name: str
    quantity_per_unit: float
    unit_of_measure: Optional[str] = "grams"
    purchase_price: float
    
    @validator('quantity_per_unit')
    def price_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Price must be greater than 0.")
        return v
    
    @validator('purchase_price')
    def price_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Price must be greater than 0.")
        return v
    

class WarehouseCreate(BaseModel):
    detail_ingredient: list[DetailIngredient]
    supplier_id: int
    
class WarehouseUpdate(BaseModel):
    ingredient_name: str
    quantity_per_unit: float
    unit_of_measure: Optional[str] = "grams"
    purchase_price: float
    supplier_id: int
    
    @validator('quantity_per_unit')
    def price_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Price must be greater than 0.")
        return v
    
    @validator('purchase_price')
    def price_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Price must be greater than 0.")
        return v