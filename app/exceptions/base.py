from fastapi import HTTPException, status
from app.schemas.general_response import *


#base exception class
class APIException(HTTPException):
    def __init__(self, status_code: int, code: str, msg: str):
        detail = ErrorDetail(code=code, msg=msg).model_dump()
        super().__init__(status_code=status_code, detail=detail)








