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
from app.schemas.po import *
from app.models.warehouses import Warehouse as WarehouseModel
from app.exceptions.purchase_order import *
from app.models.received_po_item import ReceivedPOItem as ReceivedPOItemModel
from app.models.purchase_order_items import POItem as POItemModel



import uuid

logger = LoggingService(__name__).get_logger() 


class POService(CommonService):
    def __init__(self,db:Session):
        self.db = db
        CommonService.__init__(self,db, PurchaseOrderModel)

    def create_purchase_order(self, py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Creating po with data: {pydantic_data}")

        supplier = self.db.query(SupplierModel).filter_by(id=pydantic_data['supplier_id']).first()

        #check supplier_id is exists or not
        if not supplier:
            logger.warning(f"Supplier with id {pydantic_data['supplier_id']} not exists")
            raise NotFoundException(f"Supplier with id {pydantic_data['supplier_id']} not exists")
        
        warehouse = self.db.query(WarehouseModel).filter_by(id = pydantic_data['warehouse_id']).first()

        #check warehouse with id exists or not
        if not warehouse:
            logger.warning(f"Warehouse with id {pydantic_data['warehouse_id']} not exists")
            raise NotFoundException(f"Warehouse with id {pydantic_data['warehouse_id']} not exists")
        
        
        lead_time_days = supplier.lead_time_days
        logger.info(f"supplier's lead time days: {lead_time_days}")

        #add lead days to the current data for getting expected date
        pydantic_data["expected_date"] = datetime.now(timezone.utc) + timedelta(days=lead_time_days)    
        logger.info(f"expected date set to {datetime.now(timezone.utc) + timedelta(days=lead_time_days)}")

        purchase_order = self.create_record(pydantic_data)
        logger.info(f"Adding purchase order {pydantic_data}")
        purchase_order_py_obj = POResponseSchema.model_validate(purchase_order)
        purchase_order_data = purchase_order_py_obj.model_dump()
        purchase_order_data['expected_date'] = str(purchase_order_data['expected_date'])[:10]

        return purchase_order_data
    
    def update_po_status(self,id, py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"updating po with status: {pydantic_data}")

        purchase_order_record = self.get_record_by_id(id)

        #raise exception if purchase_order_record not found
        if not purchase_order_record:
            logger.warning(f"Purchase Order with id {id} not exists")
            raise NotFoundException(f"Purchase Order with id {id} not exists")
        
        #raise exception if total_po_cost is 0 means no po item set with po
        elif not purchase_order_record.total_po_cost:
            logger.warning(f"Purchase Order with id {id} does not have any item to orderd! Please add items to PO")
            raise NotFoundException(f"Purchase Order with id {id} does not have any item to order! Please add items to PO")
        
        #raise exception if staus is same as request staus
        elif purchase_order_record.status == pydantic_data['status']:
            logger.warning(f"PO with {id }Already in {pydantic_data['status'].value}")
            raise AlreadyRegistered(f"PO with {id } Already in {pydantic_data['status'].value} state")

        #raise exception if status is drfat and trying to change with received
        if purchase_order_record.status == PurchaseOrderStatus.DRAFT and pydantic_data['status'] != PurchaseOrderStatus.ORDERD:
            logger.warning("Cannot change PO from DRAFT to RECEIVED directly. It must be ORDERED first.")
            raise InvalidStatusTransitionException("Cannot change PO from DRAFT to RECEIVED directly. It must be ORDERED first.")
        
        #raise exception if status is orderd and tryoing to change with draft
        elif purchase_order_record.status == PurchaseOrderStatus.ORDERD and pydantic_data['status'] != PurchaseOrderStatus.RECEIVED:
            logger.warning(f"PO with {id} already ordered you can't change make it draft")
            raise InvalidStatusTransitionException(f"PO with {id} already ordered you can't change make it draft")
        
        received_items = self.db.query(POItemModel).filter_by(po_id = id).all()

        received_item_record = []
        for received_item in received_items:
            item = ReceivedPOItemModel(
                product_id = received_item.product_id,
                sku = received_item.sku,
                qty = received_item.qty
            )
            received_item_record.append(item)

        self.db.add_all(received_item_record)
        try:
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DataBaseError(e)

        
        status_updated_po = self.update_record_by_id(id, py_model)
        logger.info(f"po status updated: {status_updated_po}")
        return status_updated_po






        



















        

        





