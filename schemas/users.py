from pydantic import BaseModel, ConfigDict
from models.users import Code

class UserSchema(BaseModel):
    name: str
    lastname: str
    user_code : str | None = None
    role_id: int
    email: str
    password: str
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserPublicSchema(BaseModel):
    name: str
    lastname: str
   
    role_id: int
    email: str
    
    phone: str | None = None
   
    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    phone: str | None = None
    role_id: int | None = None
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)
