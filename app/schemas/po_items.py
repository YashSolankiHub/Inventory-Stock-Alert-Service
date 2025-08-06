from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
from app.utils.validators import Validators
from uuid import UUID


class POItemCreateSchema(BaseModel):
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
    sku:str = Field(...,min_length=2)
    qty:int = Field(..., gt=0)
    unit_cost:int = Field(..., gt=0)
    po_id:UUID= Field(...)


    class Config:
        from_attributes = True
