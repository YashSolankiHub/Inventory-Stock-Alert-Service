from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
from app.utils.validators import Validators
from uuid import UUID


class SupplierCreateSchema(BaseModel):
    name:str = Field(..., min_length=2)
    email:EmailStr  
    mobile:int = Field(...)
    lead_time_days:int = Field(..., gt=0)


class SupplierResponseSchema(BaseModel):
    id:UUID
    name:str 
    email:EmailStr  
    mobile:int 
    lead_time_days:int 

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True



# class SupplierUpdateSchema(BaseModel):
#     name:str = Field(...,min_length=2)
#     email:EmailStr
#     mobile:int = Field(...)
#     lead_time_days:int = Field


