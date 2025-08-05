from config import SECRET_KEY, ALGORITHM
from datetime import timedelta,datetime, timezone
import jwt
import uuid
from enum import Enum



class TokenService:
    @staticmethod
    def create_token(data:dict, expire_delta :timedelta | None = None, token_type :str  = "access"):
        to_encode = data.copy()

        for k, v in data.items():
            if isinstance(v, uuid.UUID):
                to_encode[k] = str(v)
            elif isinstance(v, Enum):
                to_encode[k] = v.value
            else:
                to_encode[k] = v

        if expire_delta:
            expire = datetime.now(timezone.utc) + expire_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=20) 
    
        to_encode.update({"exp":expire, "type": token_type })
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
        return encoded_jwt

