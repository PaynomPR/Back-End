from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Date, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from database.config import Base

class VacationTimes(Base):
    employer_id: int
    period_id: int
    vacation_hours: float
    sicks_hours: float
    year: int
    month: int
    