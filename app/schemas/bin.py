from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional



class BinCreateSchema(BaseModel):
    name:str = Field(...,min_length=2)
    max_units:int = Field(..., gt=0, lt=1001)
    warehouse_id:UUID= Field(...)  

class BinResponseSchema(BaseModel):
    id:UUID
    name:str 
    max_units:int
    current_stock_qty:int
    warehouse_id:UUID 

    class Config:
        from_attributes= True
        
