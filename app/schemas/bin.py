from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional



class BinCreateSchema(BaseModel):
    name:str = Field(...,min_length=2)
    warehouse_id:UUID= Field(...)  
    
    

class BinResponseSchema(BaseModel):
    id:UUID
    name:str 
    warehouse_id:UUID 

    class Config:
        from_attributes= True
