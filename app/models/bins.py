from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.warehouses import Warehouse


class Bin(Base,CommonFieldsMixin):
    __tablename__ = "bins"
    name:Mapped[str] = mapped_column(String(10))
    

    warehouse:Mapped["Warehouse"] = relationship(back_populates="bins")


