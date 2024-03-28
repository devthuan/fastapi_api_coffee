from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, Field, constr, validator
from sqlalchemy import Boolean

class CartBase(BaseModel):
    product_id: int
    quantity: int
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("quantity must be greater than 0.")
        return v

