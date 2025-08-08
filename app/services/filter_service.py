from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, class_mapper, ColumnProperty, RelationshipProperty,aliased
from sqlalchemy import or_,String
from typing import List, Optional, Any
from pydantic import BaseModel
from enum import Enum
import operator
from sqlalchemy.orm import joinedload, selectinload
from pydantic import BaseModel, ConfigDict
from app.schemas.general_response import *
from app.services.search_service import SearchService
from config import OPERATOR_MAP
from app.enums.enums import FilterOperator
from app.exceptions.filter_search import *
from app.utils.logging import LoggingService

logger = LoggingService(__name__).get_logger() 


class FilterService(SearchService):
    def __init__(self,db:Session,model):
        self.db = db
        self.model = model
        # super().__init__()

    def validate_filter_parameter(self, f_model,allowed_fields):
        if f_model.page < 1:
            logger.warning(f"page : {f_model.page}")
            raise ValueErrorException("Page must be >= 1")
        if f_model.limit < 1 or f_model.limit > 100:
            logger.warning(f"limit : {f_model.limit}")
            raise ValueErrorException("Page size must be between 1 and 100")
        if f_model.sort_order not in ["asc", "desc"]:
            logger.warning(f"sort_order : {f_model.sort_order}")
            raise ValueErrorException("Sort order must be 'asc' or 'desc'")
        if f_model.sort_by is not None and f_model.sort_by not in allowed_fields:
            logger.warning(f"Invalid sort_by: {f_model.sort_by}")
            raise ValueErrorException(f"Invalid sort field: '{f_model.sort_by}'. Allowed fields are: {allowed_fields}")


# 6. Apply filters + sorting + pagination
    def apply_filter_sorting(self, filter_model, allowed_fields: List[str], db: Session):
        logger.info(f"allowed fields : {allowed_fields}")
        self.validate_filter_parameter(filter_model, allowed_fields)

        query = db.query(self.model)

        # Apply search (optional override)
        if filter_model.search:
            logger.info(f"Seach param found :{filter_model.search}")
            query = self.search_record(filter_model.search) 

        # Apply filters
        if filter_model.filters:
            logger.info(f"Filter param found : {filter_model.filters}")
            logger.info(f"flter str : {filter_model.filters}")
            parts = filter_model.filters.split(",", 2)  
            logger.info(f"Type of parts: {type(parts)}")
            logger.info(f"parts: {parts}")
            logger.info(f"len parts: {len(parts)}")

            if len(parts) != 3:
                logger.warning("Each filter must be in format: field,operator,value")
                raise ValueErrorException("Each filter must be in format: field,operator,value")

            field, operator_, value = parts

            if field not in allowed_fields:
                raise ValueErrorException(f"Invalid field name: {field}")

            field_attr = getattr(self.model, field, None)
            if not field_attr:
                raise ValueErrorException(f"Invalid field: {field}")

            # Convert value type
            if value.isdigit():
                value = int(value)
            elif value.replace(".", "", 1).isdigit():
                value = float(value)

            # Handle LIKE operator
            if operator_ == FilterOperator.LIKE:
                if not isinstance(value, str):
                    raise ValueErrorException("LIKE operator requires string")
                query = query.filter(field_attr.ilike(f"%{value}%"))
            else:
                op = OPERATOR_MAP.get(operator_)
                if not op:
                    raise ValueErrorException("Invalid Operator")
                query = query.filter(op(field_attr, value))

                # except Exception as e:
                #     raise HTTPException(status_code=400, detail=f"Invalid filter: {str(e)}")


        # Sorting
        if filter_model.sort_by:
            sort_field = getattr(self.model, filter_model.sort_by)
            if filter_model.sort_order == "desc":
                query = query.order_by(sort_field.desc())
            else:
                query = query.order_by(sort_field.asc())

        # Pagination
        offset = (filter_model.page - 1) * filter_model.limit
        total = query.count()
        results = query.offset(offset).limit(filter_model.limit).all()

        return StandardResponse(
            success=True,
            data=results,
            msg="Records fetched successfully",
            limit=filter_model.limit,
            page=filter_model.page,
            total=total
        )




