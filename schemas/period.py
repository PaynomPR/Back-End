from pydantic import BaseModel
from datetime import date
from enum import Enum

class PeriodType(str, Enum):
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"

class PeriodBase(BaseModel):
    year: int
    period_number: int
    period_start: date
    period_end: date
    period_type: PeriodType 
class PeriodCreate(PeriodBase):
    pass

class PeriodRead(PeriodBase):
    id: int
    is_deleted: bool

    class Config:
        orm_mode = True
        from_attributes = True