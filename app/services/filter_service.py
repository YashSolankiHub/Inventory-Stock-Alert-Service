from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, class_mapper, ColumnProperty, RelationshipProperty,aliased
from sqlalchemy import or_,String
from typing import List, Optional, Any
from pydantic import BaseModel
from enum import Enum
import operator
from sqlalchemy.orm import joinedload, selectinload

from pydantic import BaseModel, ConfigDict
from app.schemas.filter import FilterModel
from app.schemas.general_response import *
from app.service.search_service import SearchService
from app.enum.enum import FilterOperator
from config import OPERATOR_MAP





class MyModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    operator: FilterOperator


# 2. Filter schema
# class FilterCondition(BaseModel):
#     field: str
#     operator: FilterOperator
#     value: Any



class FilterService(SearchService):
    def __init__(self,db:Session,model):
        self.db = db
        self.model = model
        # super().__init__()

    def validate_filter_parameter(self, f_model: FilterModel):
        if f_model.page < 1:
            raise ValueError("Page must be >= 1")
        if f_model.limit < 1 or f_model.limit > 100:
            raise ValueError("Page size must be between 1 and 100")
        # if f_model.sort_order not in ["asc", "desc"]:
        #     raise ValueError("Sort order must be 'asc' or 'desc'")
        # if f_model.sort_by and f_model.sort_by not in allowed_fields:
        #     raise ValueError(f"Invalid sort field: {f_model.sort_by}. Allowed fields: {allowed_fields}")


# 6. Apply filters + sorting + pagination
    def apply_filter_sorting(self, filter_model: FilterModel, allowed_fields: List[str], db: Session, **filters):
        
        self.validate_filter_parameter(filter_model)

        query = db.query(self.model)
        if filters:
            query = self.db.query(self.model).filter_by(**filters)

        if filter_model.search:
            query = self.search_record(filter_model.search)
        else:
            query = db.query(self.model).filter_by(**filters)


        # Apply filters
        if filter_model.filters:
            try:
                parts = filter_model.filters.split(",")
                print(parts)
                if len(parts) != 3:
                    raise ValueError("Each filter must be in format: field,operator,value")
                field, operator_, value = parts
                if field not in allowed_fields:
                    raise ValueError(f"Invalid field name: {field}")
                # Handle number parsing
                if value.isdigit():
                    value = int(value)
                elif value.replace(".", "", 1).isdigit():
                    value = float(value)
                # LIKE check
                if operator_ == FilterOperator.LIKE and not isinstance(value, str):
                    raise ValueError("LIKE operator requires string")
                field_attr = getattr(self.model, field, None)
                if operator_ == FilterOperator.LIKE:
                    query = query.filter(field_attr.ilike(f"%{value}%"))
                else:
                    op = OPERATOR_MAP.get(operator_)
                    if not op:
                        raise ValueError("Invalid Operator")
                    query = query.filter(op(field_attr, value))

            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid filter: {str(e)}")

        # Apply sorting
        # if filter_model.sort_by:
        #     sort_field = getattr(self.model, filter_model.sort_by)
        #     if filter_model.sort_order == "desc":
        #         query = query.order_by(sort_field.desc())
        #     else:
        #         query = query.order_by(sort_field.asc())

        # Apply pagination
        offset = (filter_model.page - 1) * filter_model.limit
        total = query.count()
        results = query.offset(offset).limit(filter_model.limit).all()

        # return {
        #     "limit": filter_model.limit,
        #     "page": filter_model.page,
        #     "data": results,
        #     "total": total,
        # }
    
        return StandardResponse (
            success=True,
            data =results,
            msg="Records fetched successfully",
            limit= filter_model.limit,
            page = filter_model.page,
            total= total
        )



