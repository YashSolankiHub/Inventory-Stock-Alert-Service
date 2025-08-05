from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.validators import PwdContext
from fastapi import HTTPException, status, UploadFile
from sqlalchemy import and_, or_, func
from app.services.common_service import CommonService

from app.models.users import User as UserModel
from app.models.categories import Category as CategoryModel

from app.schemas.user import UserResponseSchema
from app.schemas.general_response import ErrorResponse, StandardResponse, ErrorDetail
from datetime import datetime, timezone
from app.utils.logging import LoggingService
from typing import TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.database import *
from app.exceptions.auth import *
from app.exceptions.common import *



import uuid

logger = LoggingService(__name__).get_logger() 


class CategoryService(CommonService):
    def __init__(self,db:Session):
        self.db = db
        CommonService.__init__(self,db, CategoryModel)
        # FilterService.__init__(db, CategoryModel)

    def create_category(self, py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Creating category with data: {pydantic_data}")

        is_cat_exists = self.db.query(CategoryModel).filter(func.lower(CategoryModel.name)  == func.lower(pydantic_data["name"])).first()

        #check category is exists
        if is_cat_exists:
            logger.warning(f"Category {pydantic_data['name']} already exists!")
            raise AlreadyExistsException("Category already exists!")
        
        logger.info(f"Adding new course: {pydantic_data}")
        category = self.create_record(pydantic_data)
        return category

        
        









