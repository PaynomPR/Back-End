from pydantic import BaseModel, Field, ConfigDict

class TaxeShema(BaseModel):
    name: str
    amount: float 
    required: float 
    type_taxe: float
    type_amount: float
    model_config: ConfigDict

class TaxeIDShema(TaxeShema):
    id: int
