from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT,Integer,ForeignKey
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID

if TYPE_CHECKING:
    from app.models.categories import Category


class Product(Base,CommonFieldsMixin):
    __tablename__ = "products"
    sku:Mapped[str] = mapped_column(String(20), unique=True)
    qty:Mapped[int] = mapped_column(Integer)
    cost:Mapped[int] = mapped_column(Integer)
    description:Mapped[str] = mapped_column(String(50))
    category_id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('categories.id'))

    category:Mapped["Category"] = relationship(back_populates="products")




