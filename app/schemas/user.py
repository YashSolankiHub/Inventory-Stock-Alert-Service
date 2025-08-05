from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
from app.utils.validators import Validators
from uuid import UUID

class UserResponseSchema(BaseModel):
    id:UUID
    username:str
    name:str 
    email:str
    mobile:int
    
    class Config:
        from_attributes = True 

class UserCreateSchema(BaseModel):
    username:str = Field(...,min_length=4)
    name:str = Field(..., min_length=2)
    email:EmailStr  
    mobile:int = Field(...)
    password:str = Field(..., min_length=6)

    @field_validator('mobile')
    def validate_mobile(cls, value):
        return Validators.validate_mobile(value)
        
    
    @field_validator('username')
    def validate_username(cls, value):
        return Validators.validate_username(value)
    
