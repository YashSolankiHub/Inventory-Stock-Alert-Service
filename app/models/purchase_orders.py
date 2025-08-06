from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT,Integer,ForeignKey,Enum as SQLEnum, DateTime
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
from app.enums.enums import PurchaseOrderStatus
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.suppliers import Supplier

if TYPE_CHECKING:
    from app.models.purchase_order_items import POItem


class PurchaseOrder(Base,CommonFieldsMixin):
    __tablename__ = "purchase_orders"
    total_po_cost:Mapped[int] = mapped_column(Integer, default=0)
    expected_date:Mapped[datetime]  = mapped_column(DateTime)
    status:Mapped[PurchaseOrderStatus] = mapped_column(SQLEnum(PurchaseOrderStatus), default= PurchaseOrderStatus.DRAFT)
    supplier_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('suppliers.id'))
    po_items: Mapped[List["POItem"]] = relationship(back_populates="po")

    # supplier:Mapped["Supplier"] = relationship(back_populates="pos")


