from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
from app.utils.validators import Validators
from uuid import UUID
from fastapi import Query

class FilterSearchSchema(BaseModel):
    search:str | None = None
    filters: str | None = None
    sort_order:str = "asc"
    sort_by:str | None = None
    page: int = 1 
    limit: int = 5 


def get_filter_param(
    search:Optional[str] = Query(None),
    filters: Optional[str] = Query(None, description="e.g. field,operator,value"),
    sort_order : Optional[str] = Query("asc"),
    sort_by:Optional[str] = Query(None),
    page: int = 1,
    limit: int = 5,
)->FilterSearchSchema:
    return FilterSearchSchema(
        search = search,
        filters= filters,
        sort_order= sort_order,
        sort_by=sort_by,
        page=page,
        limit=limit
    )
