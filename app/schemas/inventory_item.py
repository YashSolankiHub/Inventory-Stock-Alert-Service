from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
from app.utils.validators import Validators
from uuid import UUID

class InventoryItemCreateSchema(BaseModel):
    product_id :UUID = Field(...)
    qty:int = Field(...,gt=0)
    bin_id:UUID = Field(...)
    po_id:UUID = Field(...)

class InventoryItemResponseSchema(BaseModel):
    id:UUID
    product_id:UUID
    sku:str
    qty:int 
    bin_id:UUID 

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True






