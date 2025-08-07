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
from sqlalchemy.exc import DataError
from app.exceptions.database import *
from app.exceptions.auth import *
from app.exceptions.common import *
from app.models.products import Product as ProductModel
from app.utils.helper import generate_sku
from app.models.warehouses import Warehouse as WarehouseModel
from app.enums.enums import UserRoles
from app.models.suppliers import Supplier as SupplierModel



import uuid

logger = LoggingService(__name__).get_logger() 


class SupplierService(CommonService):
    def __init__(self, db:Session):
        self.db = db
        CommonService.__init__(self,db, SupplierModel)

    def create_supplier(self,py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Creating supplier with data: {pydantic_data}")

        supplier = self.db.query(UserModel).filter(or_(
                SupplierModel.email == pydantic_data["email"],
                SupplierModel.mobile == pydantic_data["mobile"],
                )).first()
        
        #raise exception if supplier is already registered
        if supplier:
            logger.warning(f"supllier already exists with same email/username/mobile")
            raise AlreadyRegistered("Email or mobile number is already registered!")
        
        logger.info(f"Adding new supplier: {pydantic_data}")
        supplier = self.create_record(pydantic_data)
        return supplier
        
        

        

        














        




            




        
    



