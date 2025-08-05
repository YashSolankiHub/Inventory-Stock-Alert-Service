from enum import Enum

class PurchaseOrderStatus(Enum):
    DRAFT = "draft"
    ORDERD = "ordered"
    RECEIVED = "received"


class UserRoles(str,Enum):
    ADMIN = "ADMIN"
    WAREHOUSE_MANAGER = "WAREHOUSE_MANAGER"
    CLERK = "CLERK"
    