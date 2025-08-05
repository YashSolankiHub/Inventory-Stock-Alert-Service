from pydantic import BaseModel, Field
from uuid import UUID

class CategoryCretaeSchema(BaseModel):
    name:str = Field(...,min_length=2)

class CategoryResponseSchema(BaseModel):
    id:UUID
    name:str

    class Config:
        from_attributes = True
    

