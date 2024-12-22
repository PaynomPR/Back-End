from pydantic import BaseModel, Field
from datetime import date
from schemas.time import TimeIDShema
from typing import Optional, List

class EmployersSchema(BaseModel):
    last_name: Optional[str] = Field(None, max_length=100)
    mother_last_name: Optional[str] = Field(None, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    company_id: Optional[int] = Field(None, ge=0)
    employee_type: Optional[str] = Field(None, max_length=50)
    social_security_number: Optional[str] = Field(None, max_length=11)
    marital_status: Optional[int] = Field(None, ge=0)
    work_hours: Optional[int] = Field(None, ge=0)
    address: Optional[str] = Field(None, max_length=200)
    address_state: Optional[str] = Field(None, max_length=100)
    address_country: Optional[str] = Field(None, max_length=100)
    address_number: Optional[str] = Field(None, max_length=20)
    phone_number: Optional[str] = Field(None, max_length=20)
    retention_type: Optional[str] = Field(None, max_length=20)
    smartphone_number: Optional[str] = Field(None, max_length=20)
    marbete: Optional[str] = Field(None, max_length=50)
    type: Optional[int] = Field(None, ge=0)
    date_marb: Optional[date] = None
    clipboard: Optional[str] = Field(None, max_length=100)
    exec_personal: Optional[int] = Field(None, ge=0)
    choferil: Optional[str] = Field(None, max_length=50)
    regular_time: Optional[float] = Field(None, ge=0.0)
    salary: Optional[float] = Field(None, ge=0.0)
    period_norma: Optional[int] = Field(None, ge=0)
    licence: Optional[str] = Field(None, max_length=50)
    category_cfse: Optional[str] = Field(None, max_length=50)
    gender: Optional[int] = Field(None, ge=0)
    birthday: Optional[date] = None
    date_admission: Optional[date] = None
    date_egress: Optional[date] = None
    overtime: Optional[float] = Field(None, ge=0.0)
    mealtime: Optional[float] = Field(None, ge=0.0)
    vacation_time: Optional[str]
    vacation_hours: Optional[int] = Field(None, ge=0)
    vacation_hours_monthly: Optional[int]
    vacation_date: Optional[date] = None
    sicks_date: Optional[date] = None
    sicks_hours: Optional[int] = Field(None, ge=0)    
    sick_time: Optional[str]
    sicks_hours_monthly: Optional[int] = Field(None, ge=0)
    number_dependents: Optional[int] = Field(None, ge=0)
    shared_custody: Optional[bool] = None
    number_concessions: Optional[int] = Field(None, ge=0)
    veteran: Optional[bool] = None
    type_payroll: Optional[int] = Field(None, ge=0)
    schedule_type: Optional[int] = Field(None, ge=0)
    payment_percentage: Optional[str] = Field(None, max_length=10)


class EmployerReturnIDShema(EmployersSchema):
    is_deleted: Optional[bool] = None
    id: int


class EmployerTimeShema(EmployerReturnIDShema):
    times: List[TimeIDShema] = []

    class Config:
        from_attributes = True
