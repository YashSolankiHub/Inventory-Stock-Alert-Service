from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
from app.utils.validators import Validators
from uuid import UUID
from typing import List
from app.schemas.po_items import POItemResponseSchema
from datetime import datetime


class POCreateSchema(BaseModel):
    supplier_id:UUID = Field(...)


class POResponseSchema(BaseModel):
    id:UUID
    total_po_cost:int 
    status:str
    expected_date:datetime.date
    supplier_id:UUID
    po_items:List[POItemResponseSchema]


    class Config:
        from_attributes = True
        arbitrary_types_allowed=True
