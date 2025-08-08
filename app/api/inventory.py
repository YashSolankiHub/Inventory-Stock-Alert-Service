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
from app.services.bin_service import BinService
from app.schemas.bin import *
from app.schemas.inventory_item import *
from app.services.inventory_item import InventoryItemService

logger = LoggingService(__name__).get_logger()


class InventoryRoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all inventory-related endpoints.

        This includes:
        

        Returns:
            APIRouter: Configured router with inventory routes.
        """    

        router = APIRouter(prefix="", tags=["Inventory"])

        @router.post("", response_model=StandardResponse[InventoryItemResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def add_received_po_item_in_inventory(inventory_item :InventoryItemCreateSchema, db:Session= Depends(get_db)):
            """create inventory item with data of po item id,product id, qty, bin id etc

            args: 
                inventory_item: pydantic model
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"POST :- /inventory_items endpoint called for creating item in inventorr")

            service = InventoryItemService(db)
            inventory_item = service.add_item_in_inventory(inventory_item)
            return StandardResponse(
                success=True,
                data =inventory_item,
                msg="Item added to inventory",
            )
        
        @router.get("/reports")
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def export_inventory_report(request:Request, warehouse_id: str = Query(None), db:Session = Depends(get_db)):
            logger.info(f"GET :- /inventory_items/reports endpoint called for generating reports")
            service = InventoryItemService(db)
            generate_report_path = service.export_inventory_report(warehouse_id)

            return StandardResponse(
                success=True,
                data= [],
                msg= f"Report generated successfully and save to {generate_report_path}"


            )







        

        
        
        return router
            



