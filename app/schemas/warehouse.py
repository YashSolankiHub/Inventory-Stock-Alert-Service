from pydantic import BaseModel, Field, field_validator, computed_field
from uuid import UUID
from typing import Optional, List
from app.schemas.bin import BinResponseSchema


class WarehouseCreateSchema(BaseModel):
    name:str = Field(...,min_length=2)  
    address:str = Field(..., min_length=2)
    capacity_in_sqft:int = Field(...,gt=1)
    max_bins:int = Field(...,gt=0, lt=101)
    warehouse_manager_id:UUID = Field(...)

    @computed_field
    @property
    def available_bins(cls)->int:
        return cls.max_bins


class WarehouseResponseSchema(BaseModel):
    id:UUID
    name:str 
    address:str 
    capacity_in_sqft:int 
    warehouse_manager_id:UUID 
    max_bins:int
    current_bins:int
    available_bins:int
    bins:List[BinResponseSchema]

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True

class WarehouseProductStockResponseSchema(BaseModel):
    product_id:UUID
    sku:str
    qty:int
    bin_id :UUID

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True




    

