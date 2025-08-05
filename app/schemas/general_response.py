from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")

class StandardResponse(BaseModel,Generic[T]):
    success: bool
    data: T
    msg: str
    limit: int | None = None
    page: int | None = None
    total:int | None = None


class ErrorDetail(BaseModel):
    code:str
    msg:str


class ErrorResponse(BaseModel):
    # success:bool
    error: ErrorDetail