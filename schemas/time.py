from pydantic import BaseModel, Field, ValidationError, validator
from datetime import datetime
from typing import List, Optional
from schemas.payments import PaymentIDShema
import re


class TimeShema(BaseModel):
    regular_time: str 
    regular_amount: float = Field(ge=0, description="Debe ser un valor positivo")
    over_amount: float = Field(ge=0, description="Debe ser un valor positivo")
    meal_amount: float = Field(ge=0, description="Debe ser un valor positivo")
    over_time: str
    meal_time: str 
    holiday_time: Optional[str]
    sick_time: Optional[str]
    commissions: float = Field(ge=0, description="Debe ser un valor positivo")
    asume: float = Field(ge=0, description="Debe ser un valor positivo")
    aflac : float = Field(ge=0, description="Debe ser un valor positivo")
    salary: float = Field(ge=0, description="Debe ser un valor positivo")
    refund: float = Field(ge=0, description="Debe ser un valor positivo")
    donation: float = Field(ge=0, description="Debe ser un valor positivo")

    regular_pay: float = Field(ge=0, description="Debe ser un valor positivo")
    overtime_pay: float = Field(ge=0, description="Debe ser un valor positivo")
    meal_time_pay : float = Field(ge=0, description="Debe ser un valor positivo")
    sick_pay: float = Field(ge=0, description="Debe ser un valor positivo")
    vacation_pay: float = Field(ge=0, description="Debe ser un valor positivo")
    holyday_pay: float = Field(ge=0, description="Debe ser un valor positivo")
    
    
    bonus: float = Field(ge=0, description="Debe ser un valor positivo")
    others: float = Field(ge=0, description="Debe ser un valor positivo")
    concessions: float = Field(ge=0, description="Debe ser un valor positivo")
    inability: float = Field(ge=0, description="Debe ser un valor positivo")
    medicare: float = Field(ge=0, description="Debe ser un valor positivo")
    secure_social: float = Field(ge=0, description="Debe ser un valor positivo")
    social_tips: float = Field(ge=0, description="Debe ser un valor positivo")
    tax_pr: float = Field(ge=0, description="Debe ser un valor positivo")
    choferil: float = Field(ge=0, description="Debe ser un valor positivo")
    vacation_time: str   
    tips: float = Field(ge=0, description="Debe ser un valor positivo")
    payment: List[PaymentIDShema]
    memo: str = Field(max_length=150)
    period_id: int
    accountant_id: int

    


    @validator('regular_time', 'over_time', 'meal_time', 'holiday_time', 'sick_time', 'vacation_time')
    def check_time_format(cls, value):
        if value is not None and not cls.valid_time_format(value):
            raise ValueError('El formato del tiempo es inválido')
        return value

    @validator('payment', pre=True, each_item=True)
    def check_payment_list(cls, value):
        if isinstance(value, dict):
            return PaymentIDShema(**value)
        if not isinstance(value, PaymentIDShema):
            raise TypeError(f'El item en la lista de pagos debe ser una instancia de PaymentIDShema o un diccionario válido: {value}')
        return value

    @staticmethod
    def valid_time_format(value: str) -> bool:
        return re.match(r"^(?:[0-9]+):[0-5][0-9]$", value) is not None


class TimeIDShema(TimeShema):
    created_at: datetime
    id: int

class TimeIDShema2(TimeShema):
    id: int
