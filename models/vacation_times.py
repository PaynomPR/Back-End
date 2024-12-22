from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Date, Boolean, func,Column
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from database.config import Base

class VacationTimes(Base):
    __tablename__ = "vacation_times"


    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    employer_id: Mapped[int] = mapped_column(Integer, ForeignKey("employers.id"), nullable=True, index=True)
    vacation_hours: Mapped[int] = mapped_column(Integer, nullable=True)
    paid_vacation: Mapped[bool] = mapped_column(Boolean, default=False)
    sicks_hours: Mapped[int] = mapped_column(Integer, nullable=True)
    paid_sick: Mapped[bool] = mapped_column(Boolean, default=False)
    year: Mapped[str] = mapped_column(String, nullable=True,default=0)
    month: Mapped[str] = mapped_column(String, nullable=True,default=0)
    period_id: Mapped[int] = mapped_column(Integer, nullable=True)
    
    