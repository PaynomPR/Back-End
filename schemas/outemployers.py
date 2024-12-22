from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional
from schemas.time import TimeIDShema

class OutEmployersSchema(BaseModel):
    last_name: Optional[str] = Field(None, max_length=100)
    mother_last_name: Optional[str] = Field(None, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None  # Validación automática de email
    account_number: Optional[str] = Field(None, max_length=50)
    regular_pay: Optional[float] = Field(None, ge=0.0)
    type_entity: Optional[int] = Field(None, ge=0)
    gender: Optional[int] = Field(None, ge=0)
    birthday: Optional[date] = None
    fax: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=100)
    withholding: Optional[str] = Field(None, max_length=50)
    merchant_register: Optional[str] = Field(None, max_length=50)
    employer_id: Optional[str] = Field(None, max_length=50)
    bank_account: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=200)
    address_state: Optional[str] = Field(None, max_length=100)
    address_country: Optional[str] = Field(None, max_length=100)
    address_number: Optional[str] = Field(None, max_length=20)
    phone_number: Optional[str] = Field(None, max_length=20)
    smartphone_number: Optional[str] = Field(None, max_length=20)


class OutEmployerReturnIDShema(OutEmployersSchema):
    is_deleted: Optional[bool] = None
    id: int
