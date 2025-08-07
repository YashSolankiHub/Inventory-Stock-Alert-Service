from app.exceptions.base import *
from app.schemas.general_response import *

class InvalidStatusTransitionException(APIException):
    def __init__(self, msg = "invalid status"):
        super().__init__(status_code=status.HTTP_409_CONFLICT,code="INVALID_STATUS_TRANSITION", msg= msg)
