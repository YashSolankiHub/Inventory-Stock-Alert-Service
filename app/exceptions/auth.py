from app.exceptions.base import *

class AuthExceptions(AppException):
    ...

class AlreadyRegistered(AuthExceptions):
    def __init__(self):
        detail = ErrorDetail(
                code="ALREADY_REGISTERED",
                msg="Email or username or mobile number is already registered!"
            ).model_dump()
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,detail= detail)

class Invalidcredentials(AuthExceptions):
    def __init__(self):
        detail = ErrorDetail(
                code="USERNAME_PASSWORD_INVALID",
                msg="Invalid username or password"
            ).model_dump()
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,detail= detail)