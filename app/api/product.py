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
from app.schemas.filter_search_ import *

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


        @router.post("/", response_model= StandardResponse[ProductResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def create_product(product:ProductCreateSchema , request:Request, db:Session = Depends(get_db)):
            """create product  with data of name, qty, cost,description, category_id,model, brand etc

            args: 
                product: pydantic model
                request: for extracting user's JWT token
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
        
        @router.patch("/{id}", response_model= StandardResponse[ProductResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def update_product(id:UUID, product:ProductUpdateSchema , request:Request, db:Session = Depends(get_db)):
            """update product with data of name, description,category_id,model, brand etc

            args: 
                product: pydantic model
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"PATCH :- /products/{id} endpoint called for updating product")
            service = ProductService(db)
            updated_product = service.update_product(id, product)
            return StandardResponse(
                success=True,
                data = updated_product,
                msg="product updated",
            )
        
        @router.delete("/{id}", response_model= StandardResponse[ProductResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def delete_product(id:UUID, request:Request, db:Session = Depends(get_db)):
            """delete product by id

            args: 
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"DELETE :- /products/{id} endpoint called for deleting product")
            service = ProductService(db)
            deleted_product = service.delete_product(id)
            return StandardResponse(
                success=True,
                data = deleted_product,
                msg="product deleted",
            )
        
        @router.get("/{id}", response_model= StandardResponse[ProductResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def get_product(id:UUID, request:Request, db:Session = Depends(get_db)):
            """get product by id

            args: 
                id:expect product id  
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"GET :- /products/{id} endpoint called for getting product")
            service = ProductService(db)
            product = service.get_product(id)
            return StandardResponse(
                success=True,
                data = product,
                msg="Product fetched",
            )
        
        @router.get("", response_model= StandardResponse[List[ProductResponseSchema]])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def list_products(request:Request,filters: FilterSearchSchema= Depends(get_filter_param), db:Session = Depends(get_db)):
            """get all product 

            args: 
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"GET :- /products endpoint called for getting product")
            service = ProductService(db)
            allowed_fields = ["name", "sku", "brand", "model","description"]
            products = service.list_products(filters,allowed_fields)
            return products
            
        return router




            



        


        