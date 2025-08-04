from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime,func
from sqlalchemy.ext.declarative import declared_attr
import uuid
from sqlalchemy.dialects.postgresql import UUID


class CommonFieldsMixin():
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


    @declared_attr
    def created_at(cls)->Mapped[DateTime]:
        return mapped_column(DateTime(timezone=True), server_default=func.now())
    
    @declared_attr
    def updated_at(cls)->Mapped[DateTime]:
        return mapped_column(DateTime(timezone=True), server_default=func.now())
    


    







