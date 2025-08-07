from pydantic import BaseModel, Field,computed_field
from uuid import UUID
from typing import Optional



class BinCreateSchema(BaseModel):
    name:str = Field(...,min_length=2)
    max_units:int = Field(..., gt=0, lt=1001)
    warehouse_id:UUID= Field(...)  

    @computed_field
    @property
    def available_units(cls)->int:
        return cls.max_units

class BinResponseSchema(BaseModel):
    id:UUID
    name:str 
    max_units:int
    current_stock_units:int
    available_units :int
    warehouse_id:UUID 

    class Config:
        from_attributes= True
        
