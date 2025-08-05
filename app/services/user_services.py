from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.validators import PwdContext
from fastapi import HTTPException, status, UploadFile
from sqlalchemy import and_, or_
from app.services.common_service import CommonService
from app.services.filter_service import FilterService

from app.models.users import User as UserModel

from app.schemas.user import UserResponseSchema
from app.schemas.general_response import ErrorResponse, StandardResponse, ErrorDetail
from datetime import datetime, timezone

from typing import TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.database import *
from app.exceptions.auth import *

import uuid





from app.utils.logging import LoggingService

logger = LoggingService(__name__).get_logger() 



class UserService(CommonService, FilterService):
    
    """
        inherited CommonService and FilterService
        initialized db varibale for databse interaction
        call super().__init__ for initializing CommonService constructor which take UserModel(SQLAlchemy model) and
        __name__ for logging
        pwd_context object for hashng and verify password
    """

    def __init__(self,db:Session):
        self.db = db
        super().__init__(db, UserModel)
        self.pwd_context = PwdContext()

        
        
    