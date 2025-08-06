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

logger = LoggingService(__name__).get_logger()


class ProductRoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all product-related endpoints.

        This includes:
        

        Returns:
            APIRouter: Configured router with product routes.
        """    

        router = APIRouter(prefix="", tags=["product"])


        @router.post("/products", response_model= StandardResponse[ProductResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def create_product(product:ProductCreateSchema , request:Request, db:Session = Depends(get_db)):
            """create product  with data of name, qty, cost,description, category_id,model, brand etc

            args: 
                product: pydantic model
                db: session varibale for interactios with database

            """
            logger.info(f"POST :- /products endpoint called for creating product")
            service = ProductService(db)
            product = service.create_product(product)
            return StandardResponse(
                success=True,
                data = product,
                msg="product created",
            )
        return router




            



        


        