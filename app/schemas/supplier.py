from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, Field, constr, validator
from sqlalchemy import Boolean


class SupplierCreate(BaseModel):
    name_supplier: str
    address : str
    phone :constr(min_length=10, max_length=10)
    email : EmailStr