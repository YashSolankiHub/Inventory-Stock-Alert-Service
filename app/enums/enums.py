from enum import Enum

#enum for po status
class PurchaseOrderStatus(str,Enum):
    DRAFT = "DRAFT"
    ORDERD = "ORDERED"
    RECEIVED = "RECEIVED"

#enum for user role
class UserRoles(str,Enum):
    ADMIN = "ADMIN"
    WAREHOUSE_MANAGER = "WAREHOUSE_MANAGER"
    CLERK = "CLERK"
    


# Enum for filtering
class FilterOperator(str, Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    LT = "lt"
    GTE = "gte"
    LTE = "lte"
    LIKE = "like"