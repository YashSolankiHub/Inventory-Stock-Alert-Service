from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT,Integer,ForeignKey
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from app.models.purchase_orders import PurchaseOrder


class ReceivedPOItem(Base,CommonFieldsMixin):
    __tablename__ = "received_po_items"
    product_id:Mapped[uuid.UUID]= mapped_column(UUID(as_uuid=True), ForeignKey('products.id'))
    sku:Mapped[str] = mapped_column(String(50))
    qty:Mapped[int] = mapped_column(Integer, default=0)


