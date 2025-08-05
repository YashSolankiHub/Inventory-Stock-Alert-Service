from enum import Enum

class PurchaseOrderStatus(Enum):
    DRAFT = "draft"
    ORDERD = "ordered"
    RECEIVED = "received"


class UserRoles(Enum):
    ADMIN = "admin"
    WAREHOUSE_MANAGER = "warehouse_manager"
    CLERK = "clerk"
    