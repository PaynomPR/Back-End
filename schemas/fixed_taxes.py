from pydantic import BaseModel, Field, ConfigDict

class FixedTaxeShema(BaseModel):
    name: str
    amount: float 
    limit: int

class FixedTaxeIDShema(FixedTaxeShema):
    id: int
