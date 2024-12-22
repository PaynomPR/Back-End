from pydantic import BaseModel, Field, EmailStr, validator, ValidationError, ConfigDict
from typing import Optional

class CodeSchema(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)  # Puedes ajustar la longitud según tus necesidades
    email: EmailStr  # Validación automática de email
    owner: Optional[str] = Field(None, max_length=100)
    amount: int = Field(..., ge=0, description="Debe ser un valor entero positivo")

    model_config = ConfigDict(from_attributes=True)