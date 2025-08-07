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
from app.services.po_item_service import POItemService
from app.schemas.po_items import *


logger = LoggingService(__name__).get_logger()


class POItemRoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all POItem-related endpoints.

        This includes:
        

        Returns:
            APIRouter: Configured router with POItem routes.
        """    

        router = APIRouter(prefix="", tags=["Purchase Order Items"])


        @router.post("/purchase_order_items", response_model= StandardResponse[POItemResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def create_purchase_order_item(purchase_order_item:POItemCreateSchema , request:Request, db:Session = Depends(get_db)):
            """create Purchase order item  with data of sku, 

            args: 
                PurchaseOrderIitem: pydantic model
                db: session varibale for interactios with database

            """
            logger.info(f"POST :- /Purchase_orders_items endpoint called for creating Purchase Order")
            service = POItemService(db)
            purchase_order_item = service.create_purchase_order_item(purchase_order_item)

            return StandardResponse(
                success=True,
                data =purchase_order_item,
                msg="Purchase Order created",
            )
        
        @router.delete("/purchase_order/{purchase_order_id}/purchase_order_item/{id}", response_model=StandardResponse[POItemResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def delete_po_item(purchase_order_id:UUID, id:UUID,request:Request, db:Session = Depends(get_db)):
            """delete Purchase order item , 

            args: 
                id: purchase order id
                PurchaseOrderIitem: pydantic model
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"DELETE :- /purchase_order/{purchase_order_id}/purchase_order_item/"
        "{id} endpoint called for deleting Purchase Order item")
            service = POItemService(db)
            deleted_po_item = service.delete_purchase_order_item(purchase_order_id,id)
            return StandardResponse(
                success=True,
                data =deleted_po_item,
                msg="Purchase Order item deleted",
            )


        return router




            



        


        