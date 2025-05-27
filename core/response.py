from pydantic import BaseModel
from typing import TypeVar, Optional
from pydantic.generics import GenericModel

T = TypeVar("T")

class Response(BaseModel, GenericModel[T]):
    code: int = 200
    message: str = "Success"
    data: Optional[T] = None