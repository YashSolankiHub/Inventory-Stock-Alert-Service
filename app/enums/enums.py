from enum import Enum

class PurchaseOrderStatus(str,Enum):
    DRAFT = "DRAFT"
    ORDERD = "ORDERED"
    RECEIVED = "RECEIVED"


class UserRoles(str,Enum):
    ADMIN = "ADMIN"
    WAREHOUSE_MANAGER = "WAREHOUSE_MANAGER"
    CLERK = "CLERK"
    