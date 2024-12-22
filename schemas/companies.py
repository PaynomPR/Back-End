from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import date
from schemas.employee import EmployerReturnIDShema, EmployerTimeShema
from schemas.payments import PaymentIDShema
from schemas.taxes import TaxeIDShema
from typing import Optional, List
from schemas.time import TimeIDShema


class CompaniesSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    commercial_register: Optional[str] = Field(None, max_length=100)
    jurisdiction: Optional[str] = Field(None, max_length=100)
    accountant_id: Optional[int] = Field(None, ge=0)
    email: Optional[EmailStr] = None  # Validación automática de email
    contact: Optional[str] = Field(None, max_length=100)

    w2_first_control: Optional[str] = Field(None, max_length=50)
    w2_last_control: Optional[str] = Field(None, max_length=50)
    sp_first_control: Optional[str] = Field(None, max_length=50)
    sp_last_control: Optional[str] = Field(None, max_length=50)


    contact_number: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=100)
    vacation_hours: Optional[int] = Field(None, ge=0)
    vacation_date: Optional[int] = Field(None, ge=0)
    sicks_hours: Optional[int] = Field(None, ge=0)
    choferil_number: Optional[str] = Field(None, max_length=100)
    sicks_date: Optional[int] = Field(None, ge=0)
    postal_address: Optional[str] = Field(None, max_length=200)
    zipcode_postal_address: Optional[str] = Field(None, max_length=20)
    special_contribution: Optional[str] = Field(None, max_length=20)
    country_postal_address: Optional[str] = Field(None, max_length=100)
    state_postal_addess: Optional[str] = Field(None, max_length=100)
    physical_address: Optional[str] = Field(None, max_length=200)
    zipcode_physical_address: Optional[str] = Field(None, max_length=20)
    country_physical_address: Optional[str] = Field(None, max_length=100)
    state_physical_address: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    fax_number: Optional[str] = Field(None, max_length=20)
    industrial_code: Optional[str] = Field(None, max_length=100)
    payer: Optional[str] = Field(None, max_length=100)
    desem: Optional[str] = Field(None, max_length=100)
    number_patronal: Optional[str] = Field(None, max_length=100)
    date_close: Optional[date] = None
    coml: Optional[date] = None
    employed_contribution: Optional[str] = Field(None, max_length=100)
    disabled_percent: Optional[str] = Field(None, max_length=10)
    unemployment_percentage: Optional[str] = Field(None, max_length=10)
    polize_number: Optional[str] = Field(None, max_length=100)
    driver_code: Optional[str] = Field(None, max_length=100)
    driver_rate: Optional[str] = Field(None, max_length=10)
    is_deleted: Optional[bool] = None
    tax_authority_first_control: Optional[int] = Field(None, ge=0)
    tax_authority_second_control: Optional[int] = Field(None, ge=0)


    model_config = ConfigDict(from_attributes=True)


class CompaniesIdSchema(CompaniesSchema):
    id: int


class CompaniesWithEmployersSchema(CompaniesIdSchema):
    employers: List[EmployerTimeShema] = []
    taxes: List[TaxeIDShema] = []
    

    class Config:
        from_attributes = True
