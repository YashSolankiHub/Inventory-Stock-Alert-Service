from app.exceptions.base import *
from app.schemas.general_response import *

class InvalidStatusException(APIException):
    def __init__(self, msg = "invalid status"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,code="INVALID_STATUS_TRANSITION", msg= msg)

class NoItemForPOException(APIException):
    def __init__(self, msg = "No item in po"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,code="NoItemForPO", msg= msg)



