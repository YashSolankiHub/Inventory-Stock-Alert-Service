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

logger = LoggingService(__name__).get_logger()


class UsersRoutes():
    @classmethod
    def get_router(cls)->APIRouter:
        """
        Create and return an APIRouter with all users-related endpoints.

        This includes:
        

        Returns:
            APIRouter: Configured router with auth routes.
        """    

        router = APIRouter(prefix="", tags=["auth"])

        # @router.get("",response_model= StandardResponse[List[UserResponseSchema]])
        # def list_students(
        #     search:Optional[str] = Query(None),
        #     filters: Optional[str] = Query(None, description="e.g. name,like,John"),
        #     page: int = 1,
        #     limit: int = 5, db:Session = Depends(get_db)
        # ):
        #     pass


            # #list all students with filter query parameter search, filter, page, limit 
            

            # logger.info(f"GET :- students list endpoint called")
            # logger.debug(f"Filters: search={search}, filters={filters}, page={page}, limit={limit}")
            # service = UserService(db)
            # allowed_fields = ["name", "username", "email", "mobile"]
            # students = service.list_users("student",search,filters,page, limit,allowed_fields)
            # students.msg = "Students fetch sucessfully"
            # return students
            # return StandardResponse(
            #     success=True,
            #     data=students,
            #     msg="Students fetch successfully"
            # )

        @router.get("/")
        @required_roles([UserRoles.WAREHOUSE_MANAGER, UserRoles.ADMIN])
        async def list_users(request:Request,
            db:Session = Depends(get_db)
        ):
            return db.query(UserModel).all()


        return router