from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from jwt.exceptions import InvalidTokenError
from functools import wraps
import jwt
from app.utils.logging import LoggingService
from config import SECRET_KEY, ALGORITHM



logger = LoggingService(__name__).get_logger()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def required_roles(allowed_roles: list[str]):
    def decorator(endpoint_func):
        @wraps(endpoint_func)
        async def wrapper(*args, request: Request, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                logger.warning("Missing Authorization header.")
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authorization header missing."}
                )
            
            token = await oauth2_scheme(request)
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username = payload.get('username')
                role = payload.get("role")
                type = payload.get("type")
                logger.info(f"Decoded token for user: {username} | role: {role} | type: {type}")


                if type != "access":
                    logger.warning("Invalid token type detected.")
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Could not validate credentials"}
                    )
                
                if role not in allowed_roles:
                    logger.warning(f"Permission denied to access this resource for role '{role}' ")
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied to access this resource")

            except jwt.ExpiredSignatureError:
                logger.error("Access token expired.")
                return JSONResponse(status_code=401, content="Access token expired")
            except InvalidTokenError:
                logger.error("Invalid token")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


            return await endpoint_func(*args, request=request, **kwargs)
        return wrapper
    return decorator







# token = await oauth2_scheme(request)
# It will:

# Extract the Authorization header from the incoming request.

# Looks for: Authorization: Bearer <token>

# If the header is missing or not in Bearer token format, it will raise 401 Unauthorized.

# If found, it will extract the <token> part and return it.

# That token can now be decoded/verified using JWT.