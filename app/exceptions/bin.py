from app.exceptions.base import *
from app.schemas.general_response import *


class BinCapacityExceededException(APIException):
    def __init__(self,bin_capacity, rqst_capacity ):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,code="BIN_CAPACITY_EXCEEDED", msg= f"The quantity ({rqst_capacity}) exceeds the bin's available capacity ({bin_capacity})")