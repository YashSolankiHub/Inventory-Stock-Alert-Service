from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT,Integer,ForeignKey
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
from app.models.products_categories import products_categories

if TYPE_CHECKING:
    from app.models.purchase_orders import PurchaseOrder


class Supplier(Base,CommonFieldsMixin):
    __tablename__ = "suppliers"
    name:Mapped[str] = mapped_column(String(50))
    email:Mapped[str] = mapped_column(String(50),unique=True)
    mobile:Mapped[BIGINT] = mapped_column(BIGINT, unique=True)
    lead_time_days:Mapped[int] = mapped_column(Integer)

    pos:Mapped[List["PurchaseOrder"]] = relationship(back_populates="supplier")


