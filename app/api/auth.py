from fastapi import APIRouter, Request,Depends
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
from typing import Annotated
from app.schemas.token import Token
from app.exceptions.auth import *
from datetime import timedelta
from config import ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_DAYS
from app.utils.token import TokenService


logger = LoggingService(__name__).get_logger()

class AuthRoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all auth-related endpoints.

        This includes:
        

        Returns:
            APIRouter: Configured router with auth routes.
        """



        router = APIRouter(prefix="", tags=["auth"])
        oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




        @router.post("/register/admin", response_model=StandardResponse[UserResponseSchema]) 
        async def register_warehouse_manager(user:UserCreateSchema, db:Session = Depends(get_db)):
            """
            create user with data of username,name, email, mobile, password
            user:UserCreateSchema : pydantic model
            """
            logger.info(f"POST :- auth/register/admin endpoint called for creating admin")
            required_role = UserRoles.ADMIN
            service = AuthServices(db)
            warehouse_manager = await service.create_user(user, required_role)
            return StandardResponse(
                success=True,
                data=warehouse_manager,
                msg= "Admin Created"
            )

        @router.post("/register/warehouse_manager", response_model=StandardResponse[UserResponseSchema]) 
        async def register_warehouse_manager(user:UserCreateSchema, db:Session = Depends(get_db)):
            """
            create user with data of username,name, email, mobile, password
            user:UserCreateSchema : pydantic model
            """
            logger.info(f"POST :- auth/register/warehouse_manager endpoint called for creating warehouse manager")
            required_role = UserRoles.WAREHOUSE_MANAGER
            service = AuthServices(db)
            warehouse_manager = await service.create_user(user, required_role)
            return StandardResponse(
                success=True,
                data=warehouse_manager,
                msg= "Warehouse Manager Created"
            )
        
        @router.post("/register/clerk", response_model=StandardResponse[UserResponseSchema]) 
        async def register_clerk(user:UserCreateSchema, db:Session = Depends(get_db)):
            """
            create user with data of username,name, email, mobile, password
            user:UserCreateSchema : pydantic model
            """
            logger.info(f"POST :- auth/register/clerk endpoint called for creating clerk")
            required_role = UserRoles.CLERK
            service = AuthServices(db)
            warehouse_manager = await service.create_user(user, required_role)
            return StandardResponse(
                success=True,
                data=warehouse_manager,
                msg= "Clerk Created"
            )
        

        @router.post("/login") 
        async def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db:Session = Depends(get_db))->Token:
            """login api for student which will give access token and refresh token after successfuly login

            Args:
                form_data (Annotated[OAuth2PasswordRequestForm,Depends)
                request (Request)
                db (Session, optional)

            Raises:
                Invalidcredentials

            Returns:
                Token
            """

            logger.info(f"POST :- login endpoint called for username: {form_data.username}")
            service = AuthServices(db)
            user = await service.authentic_user(form_data.username, form_data.password)
            if not user:
                logger.warning(f"invalid credentials for login")
                raise Invalidcredentials()
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

            data = {
                "id":user.id,
                "username":user.username,
                "email":user.email,
                "role":user.role
            }
            access_token = TokenService.create_token(data, expire_delta=access_token_expires, token_type="access")
            refresh_token = TokenService.create_token(data, expire_delta=refresh_token_expires, token_type="refresh")

            logger.info("Created access and refresh token")

            return Token(
                username=user.username,
                access_token=access_token,
                refresh_token= refresh_token,
                token_type="bearer"
            )
        return router
    
        








