from typing import Any

from pydantic import BaseModel


class Response(BaseModel):
    success: bool
    messsage: str
    error_code: str | None
    data: Any
