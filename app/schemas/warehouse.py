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
    

class WarehouseCreate(BaseModel):
    product_id: int
    name_product: str
    quantity_available: int
    
    @validator('quantity_available')
    def price_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("Price must be greater than 0.")
        return v
    