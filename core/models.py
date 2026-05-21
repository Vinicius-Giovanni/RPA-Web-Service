from pydantic import BaseModel, EmailStr, Field, field_validator
from .forms import as_form

@as_form
class RegisterUser(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

    @field_validator('email')
    def validate_email(cls, v):
        if not ['@'] in v:
            raise ValueError('Invalid email address')