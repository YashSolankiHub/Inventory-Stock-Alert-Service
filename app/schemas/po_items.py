from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
from app.utils.validators import Validators
from uuid import UUID


class POItemCreateSchema(BaseModel):
    product_id:UUID = Field(...)
    sku:str = Field(...,min_length=2)
    qty:int = Field(..., gt=0)
    unit_cost:int = Field(..., gt=0)
    po_id:UUID= Field(...)

    @computed_field
    @property
    def total_cost(cls)->float:
        return cls.qty * cls.unit_cost
    

class POItemResponseSchema(BaseModel):
    id:UUID
    product_id:UUID
    sku:str
    qty:int 
    unit_cost:int 
    total_cost:int 
    po_id:UUID


    class Config:
        from_attributes = True
        arbitrary_types_allowed=True

