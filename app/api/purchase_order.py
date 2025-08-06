from fastapi import APIRouter, Request,Depends, Query
from app.utils.logging import LoggingService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.general_response import *
from app.schemas.user import *
from sqlalchemy.orm import Session
from app.services.auth_services import AuthServices
from app.db.database import get_db
from app.enums.enums import UserRoles
from app.utils.validators import PwdContext
from sqlalchemy import and_
from app.models.users import User as UserModel
from typing import Annotated, List
from app.schemas.token import Token
from app.exceptions.auth import *
from datetime import timedelta
from config import ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS
from app.utils.token import TokenService
from app.core.security import required_roles
from app.schemas.categories import *
from app.services.category_services import CategoryService
from app.schemas.product import *
from app.services.product_services import ProductService
from app.schemas.warehouse import *
from app.services.warehouse_services import WarehouseService
from app.schemas.supplier import *
from app.services.supplier_services import SupplierService
from app.schemas.po import *
from app.services.po_services import POService


logger = LoggingService(__name__).get_logger()


class PORoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all PO-related endpoints.

        This includes:
        

        Returns:
            APIRouter: Configured router with PO routes.
        """    

        router = APIRouter(prefix="", tags=["Purchase Order"])


        @router.post("", response_model= StandardResponse[POResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def create_PO(PurchaseOrder:POCreateSchema , request:Request, db:Session = Depends(get_db)):
            """create Purchase order  with supplier id 

            args: 
                PurchaseOrder: pydantic model
                db: session varibale for interactios with database

            """
            logger.info(f"POST :- /Purchase_orders endpoint called for creating Purchase Order")
            service = POService(db)
            purchase_order = service.create_po(PurchaseOrder)
            purchase_order_py_obj = POResponseSchema.model_validate(purchase_order)
            purchase_order_data = purchase_order_py_obj.model_dump()

            purchase_order_data['expected_date'] = str(purchase_order_data['expected_date'])[:10]
            


            return StandardResponse(
                success=True,
                data = purchase_order_data,
                msg="Purchase Order created",
            )
        return router




            



        


        