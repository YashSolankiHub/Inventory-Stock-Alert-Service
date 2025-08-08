from app.exceptions.base import *
from app.schemas.general_response import *

class AlreadyExistsException(APIException):
    def __init__(self, msg: str = "Resource already exists", ):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,code="ALREADY_REGISTERED", msg= msg)

class NotFoundException(APIException):
    def __init__(self, msg: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,code="NOT_FOUND", msg=msg)

class PermissionDeniedException(APIException):
    def __init__(self, msg: str = "Permission denied"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, code="ACCESS_DENIED",msg=msg)

class BadRequestException(APIException):
    def __init__(self, msg: str = "Bad request", code :str= "BAD_REQUEST"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, code=code,msg=msg)
