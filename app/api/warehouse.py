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
from app.schemas.filter_search_ import *


logger = LoggingService(__name__).get_logger()


class WarehouseRoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all Warehouse-related endpoints.

        This includes:
        

        Returns:
            APIRouter: Configured router with Warehouse routes.
        """    

        router = APIRouter(prefix="", tags=["Warehouse"])


        @router.post("", response_model= StandardResponse[WarehouseResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def create_Warehouse(warehouse:WarehouseCreateSchema , request:Request, db:Session = Depends(get_db)):
            """create Warehouse  with data of name, address, capacity, warehouse_manager_id etc

            args: 
                Warehouse: pydantic model
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"POST :- /warehouses endpoint called for creating Warehouse")
            service = WarehouseService(db)
            warehouse = service.create_warehouse(warehouse)
            return StandardResponse(
                success=True,
                data = warehouse,
                msg="Warehouse created",
            )
        

        @router.get("/{id}/products_stock", response_model= StandardResponse[List[WarehouseProductStockResponseSchema]])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def get_product_stock_of_warehouse(id:UUID, request:Request, db:Session = Depends(get_db)):
            """get all products of Warehouse  

            args: 
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"GET :- /warehouses/{id}/products_stock endpoint called for getting all prodcuts stock in Warehouse")
            service = WarehouseService(db)
            warehouse_product_stocks = service.get_product_stock_of_warehouse(id)
            return StandardResponse(
                success=True,
                data = warehouse_product_stocks,
                msg="Warehouse's product stock fetched",
            )
        
        @router.get("/{id}", response_model=StandardResponse[WarehouseResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def get_warehouse_by_id(id:UUID, request:Request, db:Session = Depends(get_db)):
            """get warehouse details by id

            args: 
                id: expect warehouse id
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"GET :- /warehouses/{id} endpoint called for getting warehouse")
            service = WarehouseService(db)
            warehouse = service.get_warehouse_by_id(id)
            return StandardResponse(
                success=True,
                data = warehouse,
                msg="Warehouse fetched",
            )
        
        @router.delete("/{id}", response_model= StandardResponse[WarehouseResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def delete_warehouse(id:UUID, request:Request, db:Session = Depends(get_db)):
            """delete warehouse by id

            args: 
                id: expect warehouse id
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"DELETE :- /warehouses/{id} endpoint called for deleting warehouse")
            service = WarehouseService(db)
            deleted_warehouse = service.delete_warehouse(id)
            return StandardResponse(
                success=True,
                data = deleted_warehouse,
                msg="warehouse deleted",
            )
        

        @router.get("", response_model= StandardResponse[List[WarehouseResponseSchema]])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def list_warehouse(request:Request,filters: FilterSearchSchema= Depends(get_filter_param), db:Session = Depends(get_db)):
            """get all warehouses 

            args: 
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"GET :- /warehouses endpoint called for getting warehouses")
            service = WarehouseService(db)
            allowed_fields = ["name", "address", "max_bins", "current_bins","available_bins"]
            warehouses = service.list_warehouse(filters,allowed_fields)
            return warehouses



        return router



