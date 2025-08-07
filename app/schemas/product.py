from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from app.schemas.categories import CategoryResponseSchema

class ProductCreateSchema(BaseModel):
    name:str = Field(...,min_length=2)
    description:str = Field(...,min_length=4)
    model:Optional[str] = None
    brand:str = Field(..., min_length=2)
    category_id:UUID = Field(...)




class ProductResponseSchema(BaseModel):
    id:UUID
    sku:str
    name:str
    model:Optional[str] = None
    brand:str
    category:CategoryResponseSchema



    class Config:
        from_attributes = True
        arbitrary_types_allowed=True


class ProductUpdateSchema(BaseModel):
    name:str = Field(...,min_length=2)
    sku:Optional[str] = None
    description:str = Field(...,min_length=4)
    model:Optional[str] = None
    brand:str = Field(..., min_length=2)
