from datetime import datetime
from typing import List, Optional, Union
from fastapi import File, UploadFile
from pydantic import BaseModel, Field, validator
from sqlalchemy import Boolean

class OrderBase(BaseModel):
    user_id: int
    full_name: str
    phone_number: int
    delivery_address: str
    payment_method: str
    order_status: str
    
class OrderCreate(BaseModel):
    full_name: str
    phone_number: str
    delivery_address: str
    payment_method: str
    order_status: str
    order_details: list[dict]
    

class OrderDetailBase(BaseModel):
    product_id: int
    quantity: int
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <=0:
            raise ValueError("quantity must be greater than 0.")
        return v