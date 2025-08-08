from sqlalchemy.orm import Session, joinedload, selectinload
from pydantic import BaseModel
import jwt
from config import SECRET_KEY, ALGORITHM
from fastapi import HTTPException, status
from sqlalchemy import func,asc, desc
from sqlalchemy.exc import IntegrityError

from app.schemas.general_response import *
from datetime import datetime, timedelta,timezone
from app.schemas.general_response import *
from config import search_parameters
from sqlalchemy.orm import aliased
from sqlalchemy import or_

class SearchService():
    def __init__(self, db, model):
        super().__init__(db, model)

    def search_record(self, search_param):
        model_config = search_parameters.get(self.model)
        if not model_config:
            return 

        records = self.db.query(self.model)
        filters = []
        search_param = f"%{search_param.strip()}%"

        for column in model_config['self']:
            filter_field = getattr(self.model, column)
            filters.append(filter_field.ilike(search_param))

        for rel_attr_name, rel_fields in model_config['relationships'].items():
            rel_attr = getattr(self.model, rel_attr_name)
            related_model = rel_attr.property.mapper.class_
            alias = aliased(related_model)
            records = records.outerjoin(alias, rel_attr)
            for column in rel_fields:
                filter_field = getattr(alias, column)
                filters.append(filter_field.ilike(search_param))

        records = records.filter(or_(*filters)).distinct()
        return records