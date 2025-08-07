from app.utils.logging import LoggingService
from app.services.common_service import CommonService
from sqlalchemy.orm import Session
from app.models.users import User as UserModel
from app.utils.validators import PwdContext
from pydantic import BaseModel
from sqlalchemy import and_, or_
from app.exceptions.auth import *






logger = LoggingService(__name__).get_logger() 


class AuthServices(CommonService):
    """
        inherited CommonService 
        initialized db varibale for databse interaction
        call super().__init__ for initializing CommonService constructor which take UserModel(SQLAlchemy model) and
        __name__ for logging
        pwd_context object for hashng and verify password
    """

    def __init__(self,db:Session):
        self.db = db
        super().__init__(db, UserModel)
        self.pwd_context = PwdContext()


    async def authentic_user(self, username, password):
            """
            check if the user is authenticated or not by username and password
            
            """
            logger.info(f"Authenticating user: {username}")
            user = self.db.query(UserModel).filter(UserModel.username == username).first()

            #raise exception id user not found
            if not user:
                logger.warning(f"User with{username} not found")    
                return False
            pwd_context = PwdContext()  


            #verify password and return false if password missmatched
            if not pwd_context.verify_password(password, user.password):
                logger.warning(f"Password mismatch for user {username}")
                return False
            
            logger.info(f"User {username} authenticated successfully")
            return user

    async def create_user(self, py_model:BaseModel,role):
        """
        create user with data of pydantic model py_modal

        """
        logger.info(f"Creating user with role: {role}")
        pydantic_data = py_model.model_dump()
        logger.debug(f"Creating user with email: {pydantic_data['email']}, username: {pydantic_data['username']}, mobile: {pydantic_data['mobile']}")
        pydantic_data["role"] = role

        is_user_exists = self.db.query(UserModel).filter(or_(
                UserModel.email == pydantic_data["email"],
                UserModel.username == pydantic_data["username"],
                UserModel.mobile == pydantic_data["mobile"],
                )).first()

        #raise exception if email or, ursename or mobile already registed for user
        if is_user_exists:
            logger.warning(f"User already exists with same email/username/mobile")
            raise AlreadyRegistered()
        
        #create hashed password
        hashed_password = self.pwd_context.get_hash_password(pydantic_data['password'])
        pydantic_data['password'] = hashed_password

        user = self.create_record(pydantic_data)
        logger.info(f"User created with ID: {user.id}")
        return user


        

        
        
        




        

