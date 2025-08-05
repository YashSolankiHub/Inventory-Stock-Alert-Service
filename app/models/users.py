from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import  String, BIGINT,Enum as SQlEnum
from app.db.base import Base
from app.models.common_fields import CommonFieldsMixin
from typing import List, TYPE_CHECKING
from app.enums.enums import UserRoles


# if TYPE_CHECKING:
#     from app.models.enrollment import Enrollment
#     from app.models.otp import OTP


class User(Base,CommonFieldsMixin):
    __tablename__ = "users"
    username:Mapped[str] = mapped_column(String(20),unique=True)
    name:Mapped[str] = mapped_column(String(50))
    email:Mapped[str] = mapped_column(String(50),unique=True)
    mobile:Mapped[BIGINT] = mapped_column(BIGINT, unique=True)
    password:Mapped[str] = mapped_column(String(255))
    role:Mapped[UserRoles] = mapped_column(SQlEnum(UserRoles))









