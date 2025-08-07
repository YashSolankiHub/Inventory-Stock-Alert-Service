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

logger = LoggingService(__name__).get_logger()


class CategoryRoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all catogory-related endpoints.

        This includes:
        

        Returns:
            APIRouter: Configured router with category routes.
        """    

        router = APIRouter(prefix="", tags=["category"])

        @router.post("/categories", response_model= StandardResponse[CategoryResponseSchema])
        @required_roles([UserRoles.ADMIN, UserRoles.WAREHOUSE_MANAGER])
        async def create_category(category: CategoryCretaeSchema, request:Request, db:Session = Depends(get_db)):
            """create category with data of name

            args: 
                category: pydantic model
                request: for extracting user's JWT token

                db: session varibale for interactin database

            """
            logger.info(f"POST :- /categories endpoint called for creating category")
            service = CategoryService(db)
            category = service.create_category(category)
            return StandardResponse(
                success=True,
                data = category,
                msg="Category created",
            )
        return router




            



        


        