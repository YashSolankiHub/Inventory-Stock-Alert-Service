import os
from dotenv import load_dotenv
import operator

load_dotenv()

#postgres sql url
DATABASE_URL =  os.getenv("DATABASE_URL")



#secret key for encryption or decryption
SECRET_KEY = os.getenv("SECRET_KEY")

# algorithm to be used for encryption or decryption
ALGORITHM = "HS256"


ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 15