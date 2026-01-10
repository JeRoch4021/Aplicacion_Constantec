from pydantic import BaseModel
from typing import Any

class Response(BaseModel):
    success: bool
    messsage: str
    error_code: str | None
    data: Any


