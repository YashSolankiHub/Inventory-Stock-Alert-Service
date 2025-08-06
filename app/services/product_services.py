from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.validators import PwdContext
from fastapi import HTTPException, status, UploadFile
from sqlalchemy import and_, or_, func
from app.services.common_service import CommonService

from app.models.users import User as UserModel
from app.models.categories import Category as CategoryModel

from app.schemas.user import UserResponseSchema
from app.schemas.general_response import ErrorResponse, StandardResponse, ErrorDetail
from datetime import datetime, timezone
from app.utils.logging import LoggingService
from typing import TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import DataError
from app.exceptions.database import *
from app.exceptions.auth import *
from app.exceptions.common import *
from app.models.products import Product as ProductModel
from app.utils.helper import generate_sku



import uuid

logger = LoggingService(__name__).get_logger() 


class ProductService(CommonService):
    def __init__(self,db:Session):
        self.db = db
        CommonService.__init__(self,db, ProductModel)
        # FilterService.__init__(db, CategoryModel)

    def create_product(self, py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"Creating product with data: {pydantic_data}")


        is_product_exists = self.db.query(ProductModel).filter(func.lower(ProductModel.name)  == func.lower(pydantic_data["name"])).first()

        #check product is exists or not
        if is_product_exists:
            logger.warning(f"Product {pydantic_data['name']} already exists!")
            raise AlreadyExistsException("Product already exists!")
        

        is_cat_id_exist = self.db.query(CategoryModel).filter_by(id = pydantic_data['category_id']).first()

        #check category id is exists or notss
        if not is_cat_id_exist:
            logger.warning(f"Category with id {pydantic_data['category_id']} not found!")
            raise NotFoundException(f"Category with id {pydantic_data['category_id']} not found!")
        
        category_name  = is_cat_id_exist.name
        logger.info(f"Category Name {category_name}")

        SKU = generate_sku(
            category_name,
            pydantic_data['brand'],
            pydantic_data['name'],
            pydantic_data.get('model',None)
        )

        logger.info(f"Sku generated : {SKU}")

        pydantic_data["sku"] = SKU        
        logger.info(f"Adding new product: {pydantic_data}")
        product = self.create_record(pydantic_data)
        return product

        
        









