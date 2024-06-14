from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class Account(BaseModel):
    email: EmailStr
    name: str
    website: Optional[HttpUrl]


class AccountResponse(BaseModel):
    email: EmailStr
    name: str
    id_: int
    token: str
    website: HttpUrl = ""

    class Config:
        orm_mode = True
