from app.exceptions.base import *
from app.schemas.general_response import *


class ValueErrorException(APIException):
    def __init__(self, msg = "invalid value"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY ,code="INVALID_VALUE", msg= msg)

