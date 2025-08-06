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
        
        product_record = self.db.query(ProductModel).filter_by(sku = pydantic_data['sku']).all()

        #check product exists or not with sku
        if not product_record:
            logger.warning(f"Product with sku{pydantic_data['sku']} not found!")
            raise NotFoundException(f"Product with sku {pydantic_data['sku']} not found!")
        
        logger.info(f"Adding new po item : {pydantic_data}")
        po_item = self.create_record(pydantic_data)
        return po_item

        



        


            



        







        

        





