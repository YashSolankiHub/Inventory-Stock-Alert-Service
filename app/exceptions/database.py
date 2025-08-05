from app.exceptions.base import *
from app.schemas.general_response import *



class DataBaseError(APIException):
    def __init__(self,e):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="DB_ERROR",
            msg=f"Data base error: {str(e)}"
        )