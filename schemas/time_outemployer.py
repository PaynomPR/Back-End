from pydantic import BaseModel, ConfigDict
from schemas.payments import PaymentIDShema
from datetime import date

class OutTimeShema(BaseModel):
    regular_hours: str 
    regular_min: str  

   
    regular_pay: float

    detained: float
     

    model_config : ConfigDict(from_attributes=True)


class OutTimeIDShema(OutTimeShema):
    created_at : date
    id: int

class OutTimeIDShema2(OutTimeShema):
    
    id: int
   

   

