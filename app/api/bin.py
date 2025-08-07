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

logger = LoggingService(__name__).get_logger()


class BinRoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all Bin-related endpoints.

        This includes:
        

        Returns:
            APIRouter: Configured router with bin routes.
        """    

        router = APIRouter(prefix="", tags=["Bins"])


        @router.post("", response_model= StandardResponse[BinResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def create_bin(bin:BinCreateSchema , request:Request, db:Session = Depends(get_db)):
            """create bin  with data of name, max_units, current_stock_qty, warehouse_id etc

            args: 
                bin: pydantic model
                request: for extracting user's JWT token

                db: session varibale for interactios with database

            """
            logger.info(f"POST :- /bins endpoint called for creating bin")
            service = BinService(db)
            bin = service.create_bin(bin)
            return StandardResponse(
                success=True,
                data = bin,
                msg="Bin created",
            )
        return router




            



        


        