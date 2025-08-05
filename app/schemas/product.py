from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from app.schemas.categories import CategoryResponseSchema

class ProductCretaeSchema(BaseModel):
    name:str = Field(...,min_length=2)
    description:str = Field(...,min_length=4)
    cost:int = Field(...,gt=0)
    model:Optional[str] = None
    brand:str = Field(..., min_length=2)
    category_id:str = Field(...)







class ProductResponseSchema(BaseModel):
    id:UUID
    name:str
    model:str
    brand:str
    category:CategoryResponseSchema



    class Config:
        from_attributes = True
    

