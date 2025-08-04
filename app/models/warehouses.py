from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT, Integer
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.bins import Bin

class Warehouse(Base,CommonFieldsMixin):
    __tablename__ = "warehouses"
    name:Mapped[str] = mapped_column(String(25))
    qty:Mapped[int] = mapped_column(Integer)
    address:Mapped[str] = mapped_column(String(100))
    capicity:Mapped[int] = mapped_column(Integer)   

    bins:Mapped[List["Bin"]] = relationship(back_populates="warehouse")

    



