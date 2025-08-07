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
from app.models.purchase_orders import PurchaseOrder as PurchaseOrderModel
from app.models.suppliers import Supplier as SupplierModel
from datetime import datetime, timedelta
from app.models.purchase_order_items import POItem as POItemModel
from app.schemas.po_items import *
from app.enums.enums import PurchaseOrderStatus
from app.exceptions.database import *





import uuid

logger = LoggingService(__name__).get_logger() 


class POItemService(CommonService):
    def __init__(self,db:Session):
        self.db = db
        CommonService.__init__(self,db, POItemModel)

    def create_purchase_order_item(self, py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Creating po item  with data: {pydantic_data}")

        purchase_order_record = self.db.query(PurchaseOrderModel).filter_by(id = pydantic_data['po_id']).first()

        #check purchase order exists or not
        if not purchase_order_record:
            logger.warning(f"Purchase order with id {pydantic_data['po_id']} not found!")
            raise NotFoundException(f"Purchase order with id {pydantic_data['po_id']} not found!")
        
        product_record = self.db.query(ProductModel).filter_by(id = pydantic_data['product_id'], sku= pydantic_data['sku']).first()

        #check product exists or not with sku
        if not product_record:
            logger.warning(f"Product with id{pydantic_data['product_id']} and sku {pydantic_data['sku']} not found!")
            raise NotFoundException(f"Product with id{pydantic_data['product_id']} and sku {pydantic_data['sku']} not found!")
        
        logger.info(f"Adding new po item : {pydantic_data}")
        po_item = self.create_record(pydantic_data)

        #create POItemResponseSchema pydantic model obj for extracting total_cost value of po item
        po_item_py_obj = POItemResponseSchema.model_validate(po_item)
        po_item_data = po_item_py_obj.model_dump()

        logger.info(f"dump data: {po_item_data}")

        #add total cost of item into Purchase order's total cost
        purchase_order_record.total_po_cost = purchase_order_record.total_po_cost + po_item_data['total_cost']
        try:
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DataError(e)

        return po_item
    
    def delete_purchase_order_item(self, purchase_order_id, id):
        logger.info(f"deleting po item  with id : {id} and po id {purchase_order_id}")

        purchase_order_record = self.db.query(PurchaseOrderModel).filter_by(id = purchase_order_id ).first()

        #check purchase order with id exist or not
        if not  purchase_order_record:
            logger.warning(f"PO with id{purchase_order_id} not found!")
            raise NotFoundException(f"Purchase Order with id{purchase_order_id} not found!")
        
        if purchase_order_record.status == PurchaseOrderStatus.ORDERD:
            logger.warning(f"Purchase Order with id {id} already ordered so you can't delete any po items")
            raise AlreadyExistsException(f"Purchase Order with id {id} already ordered so you can't delete any po items")
        elif purchase_order_record.status == PurchaseOrderStatus.RECEIVED:
            logger.warning(f"Purchase Order with id {id} already received")
            raise AlreadyExistsException(f"Purchase Order with id {id} already received")


        

        purchase_order_item_record =  self.get_record_by_id(id)

        #check poitem exists or not
        if not purchase_order_item_record :
            logger.warning(f"PO item with id{id} not found!")
            raise NotFoundException(f"Purchase Order item with id {id} not found!")
        
        deleted_purchase_order_item_record = self.delete_record_by_id(id)
        #creare POItemResponseSchema pydantic model obj for extracting total cost of po item
        deleted_purchase_order_item_record_oy_obj = POItemResponseSchema.model_validate(deleted_purchase_order_item_record)
        deleted_purchase_order_item_record_data = deleted_purchase_order_item_record_oy_obj.model_dump()
        logger.info(f"dump data: {deleted_purchase_order_item_record_data}")

        purchase_order_record.total_po_cost = purchase_order_record.total_po_cost - deleted_purchase_order_item_record_data['total_cost']

        try:
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DataError(e)

        logger.info(f"Deleting purchase order with id {id}")

        return deleted_purchase_order_item_record





        

        

        
        








        



        


            



        







        

        





