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
from app.models.inventory_item import InventoryItem as InventoryItemModel
from app.services.filter_service import FilterService
from app.schemas.warehouse import *



import uuid

logger = LoggingService(__name__).get_logger() 


class WarehouseService(CommonService,FilterService):
    def __init__(self, db:Session):
        self.db = db
        CommonService.__init__(self,db, WarehouseModel)
        FilterService.__init__(self, db, WarehouseModel)

    def create_warehouse(self,py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Creating warehouse with data: {pydantic_data}")

        warehouse_record = self.db.query(WarehouseModel).filter(func.lower(WarehouseModel.name) == func.lower(pydantic_data['name'])).first()

        #raise exception if warehouse record is already registered
        if warehouse_record:
            logger.warning(f"Warehouse {pydantic_data['name']} already exists!")
            raise AlreadyExistsException('Warehosue already exists')
        
        warehouse_manager_record = self.db.query(UserModel).filter_by(id = pydantic_data['warehouse_manager_id'], role= UserRoles.WAREHOUSE_MANAGER).first()

        if not warehouse_manager_record:
            logger.warning(f"warehosue manager id with {pydantic_data['warehouse_manager_id']} does not exists")
            raise NotFoundException(f"warehosue manager id with {pydantic_data['warehouse_manager_id']} does not exists")
        
        logger.info(f"Adding new warehouse: {pydantic_data}")
        warehouse = self.create_record(pydantic_data)
        return warehouse
    
    def get_product_stock_of_warehouse(self, id):
        logger.info(f"Getting warehouse product stock with id: {id}")

        warehouse_record = self.get_record_by_id(id)

        #raise exception if warehouse record is not found
        if not warehouse_record:
            logger.warning(f"Warehouse with id {id} not exists")
            raise NotFoundException(f"Warehouse with id {id} not exists")
        
        logger.info(f"warehouse with id: {id} found")
        
        warehouse_product_stocks = self.db.query(InventoryItemModel).filter_by(warehouse_id = id).all()


        if not warehouse_product_stocks:
            logger.warning(f"Warehouse with id {id} does not have any product stocks")
            raise NotFoundException(f"Warehouse with id {id} does not have any product stocks")
        
        return warehouse_product_stocks
    
    def get_warehouse_by_id(self, id):
        logger.info(f"getting warehouse with id: {id}")
        
        warehouse_record = self.get_record_by_id(id)
        #raise exception if product not found
        if not warehouse_record:
            logger.warning(f"warehouse with id {id} not found!")
            raise NotFoundException(f"Warehouse with id {id} not found!")
        
        return warehouse_record


    def delete_warehouse(self, id):
        logger.info(f"deleting warehouse with id: {id}")

        warehouse_record = self.get_record_by_id(id)

        #raise exception if product not found
        if not warehouse_record:
            logger.warning(f"warehouse with id {id} not found!")
            raise NotFoundException(f"warehouse with id {id} not found!")
        
        deleted_warehouse = self.delete_record_by_id(id, WarehouseResponseSchema)
        logger.info(f"deleting warehouse with id: {id}")

        return deleted_warehouse
    
    def list_warehouse(self,py_model:BaseModel, allowed_fields):
        pydantic_data = py_model.model_dump()
        logger.info(f"startting process of listing warehouse with filter data {pydantic_data}")

        searched_filtered_data = self.apply_filter_sorting(py_model, allowed_fields, self.db)

        return searched_filtered_data







        
        




            




        
    



