from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import Optional, List
from app.schemas.bin import BinResponseSchema


class WarehouseCreateSchema(BaseModel):
    name:str = Field(...,min_length=2)  
    address:str = Field(..., min_length=2)
    capacity_in_sqft:int = Field(...,gt=1)
    max_bins:int = Field(...,gt=0, lt=101)
    warehouse_manager_id:UUID = Field(...)


    

class WarehouseResponseSchema(BaseModel):
    id:UUID
    name:str 
    address:str 
    capacity_in_sqft:int 
    warehouse_manager_id:UUID 
    max_bins:int
    current_bins:int
    bins:List[BinResponseSchema]

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True

    

