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
from app.schemas.product import *



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


        product_record = self.db.query(ProductModel).filter(func.lower(ProductModel.name)  == func.lower(pydantic_data["name"])).first()

        #raise exception if product_record is already registered
        if product_record:
            logger.warning(f"Product {pydantic_data['name']} already exists!")
            raise AlreadyExistsException("Product already exists!")
        

        category_record = self.db.query(CategoryModel).filter_by(id = pydantic_data['category_id']).first()

        #raise exception if category_record not found
        if not category_record:
            logger.warning(f"Category with id {pydantic_data['category_id']} not found!")
            raise NotFoundException(f"Category with id {pydantic_data['category_id']} not found!")
        
        category_name  = category_record.name
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
    
    def get_product(self, id):
        logger.info(f"getting product with id: {id}")
        
        product_record = self.get_record_by_id(id)
        #raise exception if product not found
        if not product_record:
            logger.warning(f"Product with id {id} not found!")
            raise NotFoundException(f"Product with id {id} not found!")
        
        return product_record

    
    def update_product(self, id, py_model:BaseModel):
        pydantic_data = py_model.model_dump()
        logger.info(f"updating product with data: {pydantic_data}")

        product_record = self.get_record_by_id(id)

        #raise exception if product not found
        if not product_record:
            logger.warning(f"Product with id {id} not found!")
            raise NotFoundException(f"Product with id {id} not found!")
        
        #get category for generating sku
        category = self.db.query(CategoryModel).filter_by(id = product_record.category_id ).first()

        updated_product_sku = generate_sku(category.name,product_record.brand,pydantic_data['name'],product_record.model)
        logger.info(f"Updated product sku{updated_product_sku}")

        #update product sku
        pydantic_data['sku'] = updated_product_sku

        py_model =ProductUpdateSchema (
            **pydantic_data
        )

        updated_product = self.update_record_by_id(id,py_model)
        logger.info(f"updating product with id: {id}")

        return updated_product
    
    def delete_product(self, id):
        logger.info(f"deleting product with id: {id}")

        product_record = self.get_record_by_id(id)

        #raise exception if product not found
        if not product_record:
            logger.warning(f"Product with id {id} not found!")
            raise NotFoundException(f"Product with id {id} not found!")
        
        deleted_product = self.delete_record_by_id(id, ProductResponseSchema )
        logger.info(f"deleting product with id: {id}")

        return deleted_product
    
    def list_products(self):
        pass












        
        








        
        









