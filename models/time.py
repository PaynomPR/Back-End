from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Date, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database.config import Base
from models import periods

class Time(Base):
    __tablename__ = "employers_time"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    regular_amount: Mapped[float] = mapped_column(nullable=True, default=0)
    over_amount: Mapped[float] = mapped_column(nullable=True, default=0)
    meal_amount: Mapped[float] = mapped_column(nullable=True, default=0)
    salary : Mapped[float] = mapped_column(nullable=True)

    regular_time: Mapped[str] = mapped_column(String, nullable=True, default="00:00")
    over_time: Mapped[str] = mapped_column(String, nullable=True, default="00:00")
    meal_time: Mapped[str] = mapped_column(String, nullable=True, default="00:00")
    sick_time: Mapped[str] = mapped_column(String, nullable=True, default="00:00")
    holiday_time: Mapped[str] = mapped_column(String, nullable=True, default="00:00")
    vacation_time: Mapped[str] = mapped_column(String, nullable=True, default="00:00")    
    donation: Mapped[float] = mapped_column(nullable=True, default=0)
    aflac: Mapped[float] = mapped_column(nullable=True, default=0)
    commissions: Mapped[float] = mapped_column(nullable=True, default=0)
    choferil: Mapped[float] = mapped_column(nullable=True, default=0)
    concessions: Mapped[float] = mapped_column(nullable=True, default=0)
    tips: Mapped[float] = mapped_column(nullable=True, default=0)
    asume: Mapped[float] = mapped_column(nullable=True, default=0)

    inability: Mapped[float] = mapped_column(nullable=True, default=0)
    medicare: Mapped[float] = mapped_column(nullable=True, default=0)
    others: Mapped[float] = mapped_column(nullable=True, default=0)
    refund: Mapped[float] = mapped_column(nullable=True, default=0)
    bonus: Mapped[float] = mapped_column(nullable=True, default=0)
    employer_retained: Mapped[str] = mapped_column(nullable=True, default=0)
    regular_pay: Mapped[float] = mapped_column(nullable=True, default=0)
    over_pay: Mapped[float] = mapped_column(nullable=True, default=0)
    vacation_pay: Mapped[float] = mapped_column(nullable=True, default=0)
    vacation_acum_hours: Mapped[str] = mapped_column(nullable=True, default=0)
    sicks_acum_hours: Mapped[str] = mapped_column(nullable=True, default=0)
    hours_worked_salary: Mapped[int] = mapped_column(Integer, nullable=True)
    meal_pay: Mapped[float] = mapped_column(nullable=True, default=0)
    sick_pay: Mapped[float] = mapped_column(nullable=True, default=0)
    holyday_pay: Mapped[float] = mapped_column(nullable=True, default=0)

    secure_social: Mapped[float] = mapped_column(nullable=True, default=0)
    social_tips: Mapped[float] = mapped_column(nullable=True, default=0)
    tax_pr: Mapped[float] = mapped_column(nullable=True, default=0)
    accountant_id: Mapped[int] = mapped_column(Integer, ForeignKey("accountants.id"), nullable=True, index=True)

    employer_id: Mapped[int] = mapped_column(Integer, ForeignKey("employers.id"), nullable=True, index=True)
    period_id: Mapped[int] = mapped_column(Integer, ForeignKey("periods.id"), nullable=True, index=True)
    employer = relationship("Employers", back_populates="time")
    payment = relationship("Payments", back_populates="time")
    period = relationship("Period", back_populates="time")

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=True)
    deleted_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    update_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
    memo: Mapped[str] = mapped_column(String, nullable=True)

    total_payment: Mapped[float] = mapped_column(nullable=True, default=0)    
