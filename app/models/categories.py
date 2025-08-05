from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.products import Product


class Category(Base,CommonFieldsMixin):
    __tablename__ = "categories"
    name:Mapped[str] = mapped_column(String(20), unique=True)
    products:Mapped[List["Product"]] = relationship(back_populates="category")