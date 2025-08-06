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
        @required_roles([UserRoles.ADMIN])
        async def create_Warehouse(warehouse:WarehouseCreateSchema , request:Request, db:Session = Depends(get_db)):
            """create Warehouse  with data of name, address, capacity, warehouse_manager_id etc

            args: 
                Warehouse: pydantic model
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
        return router




            



        


        