from app.exceptions.base import *

class AuthExceptions(APIException):
    ...



class AlreadyRegistered(AuthExceptions):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="ALREADY_REGISTERED",
            msg="Email or username or mobile number is already registered!"
        )


class Invalidcredentials(AuthExceptions):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="USERNAME_PASSWORD_INVALID",
            msg="Invalid username or password"
        )
