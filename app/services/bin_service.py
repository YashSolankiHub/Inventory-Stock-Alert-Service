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
from app.models.bins import Bin as BinModel



import uuid

logger = LoggingService(__name__).get_logger() 


class BinService(CommonService):
    def __init__(self, db:Session):
        self.db = db
        CommonService.__init__(self,db, BinModel)

    def create_bin(self,py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Creating bin with data: {pydantic_data}")

        warehouse_record = self.db.query(WarehouseModel).filter_by(id = pydantic_data['warehouse_id']).first()

        #raise exception if warehouse not exists
        if not warehouse_record :
            logger.warning(f"Warehouse with id  {pydantic_data['warehouse_id']} not exists!")
            raise NotFoundException(f"Warehouse with id  {pydantic_data['warehouse_id']} not exists!")

        bin_record = self.db.query(BinModel).filter(func.lower(BinModel.name) == func.lower(pydantic_data['name'])).first()

        #raise exception if bin record is already registered
        if bin_record:
            logger.warning(f"Bin {pydantic_data['name']} already exists!")
            raise AlreadyExistsException('Bin already exists')

        
        logger.info(f"Adding new bin: {pydantic_data}")
        warehouse = self.create_record(pydantic_data)
        return warehouse
        




            




        
    



