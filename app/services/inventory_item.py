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
from app.models.inventory_item import InventoryItem as InventoryItemModel
from app.models.purchase_order_items import POItem as POItemModel
from app.exceptions.bin import *
from app.models.received_po_item import ReceivedPOItem as ReceivedPOItemModel



import uuid

logger = LoggingService(__name__).get_logger() 


class InventoryItemService(CommonService):
    def __init__(self, db:Session):
        self.db = db
        CommonService.__init__(self,db, InventoryItemModel)

    def add_item_in_inventory(self, py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Adding item in inventory with data: {pydantic_data}")

        received_item_record = self.db.query(ReceivedPOItemModel).filter_by(id = pydantic_data['product_id']).first()

        #raise exception if received_item_record not found
        if not received_item_record:
            logger.warning(f"Received item  with id{pydantic_data['product_id']} not found!")
            raise NotFoundException(f"Received item  with id{pydantic_data['product_id']} not found!")
        
        bin_record = self.db.query(BinModel).filter_by(id = pydantic_data['bin_id']).first()

        #raise exception if bin reocrd not found
        if not bin_record:
            logger.warning(f"Bin with id{pydantic_data['bin_id']} not found!")
            raise NotFoundException(f"Bin with id{pydantic_data['bin_id']} not found!")
        
        bin_capacity = bin_record.max_units
        
        #raise exception if request qty is greater than bin capicity
        if pydantic_data['qty'] > bin_capacity:
            logger.warning(f"The quantity ({pydantic_data['qty']}) exceeds the bin's available capacity ({bin_capacity})")
            raise BinCapacityExceededException(bin_capacity, pydantic_data['qty'])
        
        pydantic_data["product_id"] = received_item_record.product_id
        logger.info(f"Adding item in inventory with data: {pydantic_data}")
        inventory_item = self.create_record(pydantic_data)
        return inventory_item
    

