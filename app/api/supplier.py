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


logger = LoggingService(__name__).get_logger()


class SupplierRoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all Supplier-related endpoints.

        This includes:
        - create supplier

        Returns:
            APIRouter: Configured router with Supplier routes.
        """    
        router = APIRouter(prefix="", tags=["Supplier"])


        @router.post("", response_model= StandardResponse[SupplierResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def create_supplier(supplier:SupplierCreateSchema , request:Request, db:Session = Depends(get_db)):
            """create Supplier  with data of name, email,mobile,lead_time_days etc

            args: 
                Supplier: pydantic model
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"POST :- /suppliers endpoint called for creating Supplier")
            service = SupplierService(db)
            supplier = service.create_supplier(supplier)
            return StandardResponse(
                success=True,
                data = supplier,
                msg="Supplier created",
            )
        
        @router.get("/{id}", response_model=StandardResponse[SupplierResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def get_supplier_by_id(id:UUID , request:Request, db:Session = Depends(get_db)):
            """get  Supplierby id 

            args: 
                id: expect supllier id
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"GET :- /suppliers/{id} endpoint called for getting Supplier")
            service = SupplierService(db)
            supplier = service.get_supplier_by_id(id)

            return StandardResponse(
                success= True,
                data= supplier,
                msg= "Supplier Fetched"
            )
        @router.patch("/{id}", response_model= StandardResponse[SupplierUpdateSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def update_supplier(id:UUID, supplier:SupplierUpdateSchema , request:Request, db:Session = Depends(get_db)):
            """update supplier with data of name, email, mobile, lead_time_days 

            args: 
                id: expect supplier id
                request: for extracting user's JWT token
                db: session varibale for interactios with database

            """
            logger.info(f"PATCH :- /suppliers/{id} endpoint called for updating supplier")
            service = SupplierService(db)
            updated_supplier = service.update_supplier(id,supplier)

            return StandardResponse(
                success= True,
                data= updated_supplier,
                msg= "Supplier updated"
            )
        return router


