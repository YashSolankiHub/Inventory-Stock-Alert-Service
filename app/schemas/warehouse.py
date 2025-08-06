from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional, List
from app.schemas.bin import BinResponseSchema


class WarehouseCreateSchema(BaseModel):
    name:str = Field(...,min_length=2)  
    address:str = Field(..., min_length=2)
    capacity_in_sqft:int = Field(...,gt=1)
    warehouse_manager_id:UUID = Field(...)
    

class WarehouseResponseSchema(BaseModel):
    id:UUID
    name:str 
    address:str 
    capacity_in_sqft:int 
    warehouse_manager_id:UUID 
    bins:List[BinResponseSchema]



    class Config:
        from_attributes = True
    

