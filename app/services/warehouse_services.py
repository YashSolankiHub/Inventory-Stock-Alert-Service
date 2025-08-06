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



import uuid

logger = LoggingService(__name__).get_logger() 


class WarehouseService(CommonService):
    def __init__(self, db:Session):
        self.db = db
        CommonService.__init__(self,db, WarehouseModel)

    def create_warehouse(self,py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Creating product with data: {pydantic_data}")

        is_warehouse_exists = self.db.query(WarehouseModel).filter(func.lower(WarehouseModel.name) == func.lower(pydantic_data['name'])).first()

        #check warehouse already exists or not
        if is_warehouse_exists:
            logger.warning(f"Warehouse {pydantic_data['name']} already exists!")
            raise AlreadyExistsException('Warehosue already exists')
        
        warehouse_manager_id = self.db.query(UserModel).filter_by(id = pydantic_data['warehouse_manager_id'], role= UserRoles.WAREHOUSE_MANAGER).first()

        if not warehouse_manager_id:
            logger.warning(f"warehosue manager id with {pydantic_data['warehouse_manager_id']} does not exists")
            raise NotFoundException(f"warehosue manager id with {pydantic_data['warehouse_manager_id']} does not exists")
        
        logger.info(f"Adding new warehouse: {pydantic_data}")
        warehouse = self.create_record(pydantic_data)
        return warehouse
        




            




        
    



