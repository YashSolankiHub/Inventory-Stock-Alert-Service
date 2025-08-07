from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT,Integer,ForeignKey
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from app.models.purchase_orders import PurchaseOrder


class POItem(Base,CommonFieldsMixin):
    __tablename__ = "purchase_order_items"
    product_id:Mapped[uuid.UUID]= mapped_column(UUID(as_uuid=True), ForeignKey('products.id'))
    sku:Mapped[str] = mapped_column(String(50))
    qty:Mapped[int] = mapped_column(Integer, default=0)
    unit_cost:Mapped[int] = mapped_column(Integer)
    total_cost:Mapped[int] = mapped_column(Integer)
    po_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('purchase_orders.id'))

    po:Mapped["PurchaseOrder"] = relationship(back_populates="po_items")

