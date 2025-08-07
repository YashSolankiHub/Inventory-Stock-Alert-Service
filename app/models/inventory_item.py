from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT,Integer,ForeignKey
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID


class InventoryItem(Base,CommonFieldsMixin):
    __tablename__ = "inventory_items"
    po_item_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("purchase_order_items.id"))
    product_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
    qty:Mapped[int] = mapped_column(Integer)
    bin_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('bins.id'))
    

