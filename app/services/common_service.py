from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.schemas.general_response import *
from app.exceptions.database import DataBaseError


class CommonService():
    def __init__(self,db:Session, model):
        self.db = db
        self.model = model

        # super().__init__()

    # def get_all_records(self):
    #     try: 
    #         records = self.db.query(self.model).all()
    #         return records
    #     except SQLAlchemyError as e:
    #         raise DataBaseError(e)
    
    def get_all_records(self, **filters):
        try:
            query = self.db.query(self.model)
            if filters:
                query = query.filter_by(**filters)  
            records = query.all()
            return records
        except SQLAlchemyError as e:
            raise DataBaseError(e)

    
    def get_record_by_id(self,id):
        try:
            record = self.db.get(self.model, id)
            return record
        except SQLAlchemyError as e:
            raise DataBaseError(e)

    
    def create_record(self, py_model):
        record = self.model(**py_model)
        try:
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            return record
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DataBaseError(e)
    
    def delete_record_by_id(self, id,schema:BaseModel):
        deleted_record = self.db.get(self.model,id)
        try:
            data = schema.model_validate(deleted_record)
            self.db.delete(deleted_record)
            self.db.commit()
            return data
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DataBaseError(e)
    
    def update_record_by_id(self, id, py_model):
        model_data = self.get_record_by_id(id)
        pydantic_data = py_model.model_dump()
        pydantic_data["updated_at"] = datetime.now(timezone.utc)
        print(pydantic_data)
        try:
            for column, value in pydantic_data.items():
                setattr(model_data, column, value)

            self.db.commit()
            self.db.refresh(model_data)
            return model_data
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DataBaseError(e)

        


