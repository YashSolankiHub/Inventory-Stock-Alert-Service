from fastapi import HTTPException, status
from app.schemas.general_response import *


class AppException(HTTPException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)





