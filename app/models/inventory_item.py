from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT,Integer,ForeignKey
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID


class InventoryItem(Base,CommonFieldsMixin):
    __tablename__ = "inventory_items"
    product_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
    sku:Mapped[str] = mapped_column(String(50))
    qty:Mapped[int] = mapped_column(Integer)
    bin_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('bins.id'))
    warehouse_id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('warehouses.id'))


