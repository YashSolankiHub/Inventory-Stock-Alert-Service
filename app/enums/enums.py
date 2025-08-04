from enum import Enum

class PurchaseOrderStatus(Enum):
    DRAFT = "draft"
    ORDERD = "ordered"
    RECEIVED = "received"

    