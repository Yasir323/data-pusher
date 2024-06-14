from enum import Enum
from typing import Dict

from pydantic import BaseModel, HttpUrl


class HttpMethod(Enum):
    Get = "GET"
    Post = "POST"
    Put = "PUT"
    Patch = "PATCH"
    Delete = "DELETE"


class Destination(BaseModel):
    account_id: int
    url: HttpUrl
    http_method: HttpMethod
    headers: Dict[str, str]


class DestinationResponse(BaseModel):
    account_id: int
    destination_id: int
    url: HttpUrl
    http_method: HttpMethod
    headers: Dict[str, str]

    class Config:
        orm_mode = True
