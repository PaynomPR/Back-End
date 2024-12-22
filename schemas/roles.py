from pydantic import BaseModel, ConfigDict, Field


class RoleSchema(BaseModel):
    role: str = Field(max_length=50)

    model_config = ConfigDict(from_attributes=True)
