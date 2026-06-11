from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

class RegisterUserDTO(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class LoginDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
