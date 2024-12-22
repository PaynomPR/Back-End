from pydantic import BaseModel, Field, EmailStr, validator, ValidationError
from typing import Optional
import re


class Accountants(BaseModel):
    code_id: Optional[int] = None
    email: Optional[EmailStr] = None  # Validación automática de email
    name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    first_last_name: Optional[str] = Field(None, max_length=100)
    second_last_name: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = None
    country: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    zip_code: Optional[str] = Field(None, max_length=20)
    physical_country: Optional[str] = Field(None, max_length=100)
    physical_state: Optional[str] = Field(None, max_length=100)
    physical_address: Optional[str] = Field(None, max_length=100)
    physical_zip_code: Optional[str] = Field(None, max_length=100)
    identidad_ssa: Optional[str] = Field(None, max_length=100)
    identidad_bso: Optional[str] = Field(None, max_length=100)
    identidad_efile: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=200)
    employer_insurance_number: Optional[str] = Field(None, max_length=100)
    user_id: Optional[int] = None

    @validator('phone')
    def validate_phone(cls, value):
        if value and not cls.is_valid_phone(value):
            raise ValueError('El número de teléfono no es válido')
        return value

    @staticmethod
    def is_valid_phone(value: str) -> bool:
        pattern = re.compile(r'^(?:\+1)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}$')
        return bool(pattern.match(value))