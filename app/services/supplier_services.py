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
from app.services.filter_service import FilterService



import uuid

logger = LoggingService(__name__).get_logger() 


class SupplierService(CommonService, FilterService):
    def __init__(self, db:Session):
        self.db = db
        CommonService.__init__(self,db, SupplierModel)
        FilterService.__init__(self, db, SupplierModel )

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
    
    def get_supplier_by_id(self, id):
        logger.info(f"getting supplier with id :{id}")

        supplier_record = self.get_record_by_id(id)

        if not supplier_record:
            logger.warning(f"Suplier with id {id} not exists")
            raise NotFoundException(f"Suplier with id {id} not exists")
        
        return supplier_record
    
    def update_supplier(self, id, py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"updating supplier with data: {pydantic_data}")

        supplier_record = self.get_record_by_id(id)

        #raise exception if supplier not found
        if not supplier_record:
            logger.warning(f"supplier with id {id} not found!")
            raise NotFoundException(f"supplier with id {id} not found!")

        updated_supplier = self.update_record_by_id(id,py_model)
        logger.info(f"updating supplier with id: {id}")

        return updated_supplier
    
    def list_suppliers(self,py_model:BaseModel, allowed_fields):
        pydantic_data = py_model.model_dump()
        logger.info(f"startting process of listing suppliers with filter data {pydantic_data}")

        searched_filtered_data = self.apply_filter_sorting(py_model, allowed_fields, self.db)

        return searched_filtered_data
    






        
        

        

        














        




            




        
    



