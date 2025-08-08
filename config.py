import os
from dotenv import load_dotenv
import operator
from app.enums.enums import FilterOperator
from app.models.products import Product

load_dotenv()

#postgres sql url
DATABASE_URL =  os.getenv("DATABASE_URL")



#secret key for encryption or decryption
SECRET_KEY = os.getenv("SECRET_KEY")

# algorithm to be used for encryption or decryption
ALGORITHM = "HS256"


ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 15


#operator mapping for filtering
OPERATOR_MAP = {
    FilterOperator.EQ: operator.eq,
    FilterOperator.NE: operator.ne,
    FilterOperator.GT: operator.gt,
    FilterOperator.LT: operator.lt,
    FilterOperator.GTE: operator.ge,
    FilterOperator.LTE: operator.le,
}


search_parameters = {
    Product: {
        'self': ["name", "sku", "brand", "model","description"],
        'relationships': {
            'category':['name']
        }
    },}