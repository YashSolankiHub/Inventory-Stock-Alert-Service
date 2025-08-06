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



import uuid

logger = LoggingService(__name__).get_logger() 


class POService(CommonService):
    def __init__(self,db:Session):
        self.db = db
        CommonService.__init__(self,db, PurchaseOrderModel)

    def create_po(self, py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Creating po with data: {pydantic_data}")

        supplier = self.db.query(SupplierModel).filter_by(id=pydantic_data['supplier_id']).first()

        #check supplier_id is exists or not
        if not supplier:
            logger.warning(f"Supplier with id {pydantic_data['supplier_id']} not exists")
            raise NotFoundException(f"Supplier with id {pydantic_data['supplier_id']} not exists")
        
        lead_time_days = supplier.lead_time_days
        logger.info(f"supplier's lead time days: {lead_time_days}")

        pydantic_data["expected_date"] = datetime.now(timezone.utc) + timedelta(days=lead_time_days) 
        logger.info(f"expected date set to {datetime.now(timezone.utc) + timedelta(days=lead_time_days)}")

        purchase_order = self.create_record(pydantic_data)
        logger.info(f"Adding purchase order {pydantic_data}")

        return purchase_order








        

        





