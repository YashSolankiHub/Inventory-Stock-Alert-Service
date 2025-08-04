from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT,Integer,ForeignKey
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
from sqlalchemy import Enum as SQLEnum
from app.enums.enums import PurchaseOrderStatus
import uuid
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from app.models.suppliers import Supplier


class PurchaseOrder(Base,CommonFieldsMixin):
    __tablename__ = "purchase_orders.py"
    product_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('products.id'))
    qty:Mapped[int] = mapped_column(Integer)
    unit_cost:Mapped[int] = mapped_column(Integer)
    total_cost:Mapped[int] = mapped_column(Integer)
    #remaining thing:- expected_date:Mapped 
    lead_time_days:Mapped[int] = mapped_column(Integer)
    status:Mapped[PurchaseOrderStatus] = mapped_column(SQLEnum(PurchaseOrderStatus), default= PurchaseOrderStatus.DRAFT)
    supplier_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('suppliers.id'))
    supplier: Mapped["Supplier"] = relationship(back_populates="pos")
