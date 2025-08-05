from app.exceptions.base import *
from app.schemas.general_response import *


class DataBaseError(AppException):
    def __init__(self, e):
        detail = ErrorDetail(
                code="DB_ERROR",
                msg=f"Data base error: {str(e)}"
            ).model_dump()
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail= detail)