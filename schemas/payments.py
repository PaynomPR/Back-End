from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PaymentShema(BaseModel):
    name: str
    amount: float   
    value: float   
    required: float  
    type_taxe: float
    is_active: Optional[bool] = None
    type_amount: float
    model_config: ConfigDict

class PaymentIDShema(PaymentShema):
    id: int

