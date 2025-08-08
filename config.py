import os
from dotenv import load_dotenv
import operator
from app.enums.enums import FilterOperator
from app.models.products import Product
from app.models.warehouses import Warehouse
from app.models.inventory_item import InventoryItem

load_dotenv()

#postgres sql url
DATABASE_URL =  os.getenv("DATABASE_URL")



#secret key for encryption or decryption
SECRET_KEY = os.getenv("SECRET_KEY")

# algorithm to be used for encryption or decryption
ALGORITHM = "HS256"

#email password
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

ACCESS_TOKEN_EXPIRE_MINUTES = 1200
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
    },
    Warehouse :{
        'self' : ["name", "address", "max_bins", "current_bins","available_bins"],
        'relationships': {
            'bins' : ["name", "max_units", "current_stock_units", "available_units"]
        }
    },
    InventoryItem :{
        'self' :["sku", "qty"],
        'relationships': {}

    }


    }
