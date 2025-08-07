from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT, ForeignKey, Integer
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from app.models.warehouses import Warehouse


class Bin(Base,CommonFieldsMixin):
    __tablename__ = "bins"
    name:Mapped[str] = mapped_column(String(10))
    max_units:Mapped[int] = mapped_column(Integer)
    current_stock_units :Mapped[int] = mapped_column(Integer, default=0)
    available_units :Mapped[int] = mapped_column(Integer)
    warehouse_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey('warehouses.id'))

    warehouse:Mapped["Warehouse"] = relationship(back_populates="bins")


