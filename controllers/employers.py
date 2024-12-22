from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Date, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database.config import Base


class Employers(Base):
    __tablename__ = "employers"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    mother_last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    company_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("companies.id"), nullable=True, index=True
    )
    time = relationship("Time", back_populates="employer")

    company = relationship("Companies", back_populates="employers")
    marbete: Mapped[str] = mapped_column(String(50), nullable=True)
    type: Mapped[int] = mapped_column(
        nullable=True,
    )
    date_marb: Mapped[TIMESTAMP] = mapped_column(Date(), nullable=True)
    clipboard: Mapped[str] = mapped_column(String(50), nullable=True)
    exec_personal: Mapped[int] = mapped_column(
        nullable=True,
    )
    choferil: Mapped[str] = mapped_column(String(50), nullable=True)
    regular_time: Mapped[float] = mapped_column(nullable=True)
    period_norma: Mapped[int] = mapped_column(
        nullable=True,
    )
    licence: Mapped[str] = mapped_column(String(50), nullable=True)
    category_cfse: Mapped[str] = mapped_column(String(50), nullable=True)
    gender: Mapped[int] = mapped_column(
        nullable=True,
    )
    salary : Mapped[float] = mapped_column(nullable=True)
    birthday: Mapped[TIMESTAMP] = mapped_column(Date(), nullable=True)
    date_admission: Mapped[TIMESTAMP] = mapped_column(Date(), nullable=True)
    date_egress: Mapped[TIMESTAMP] = mapped_column(Date(), nullable=True)
    overtime: Mapped[float] = mapped_column(nullable=True)
    mealtime: Mapped[float] = mapped_column(nullable=True)

    vacation_time: Mapped[str] = mapped_column(String, nullable=True, default="00:00")    
    sick_time: Mapped[str] = mapped_column(String, nullable=True, default="00:00")
    vacation_hours: Mapped[int] = mapped_column(nullable=True)

    vacation_hours_monthly: Mapped[int] = mapped_column( nullable=True)
    sicks_date: Mapped[str] = mapped_column(String, nullable=True, default="00:00")
    vacation_date: Mapped[str] = mapped_column(String, nullable=True, default="00:00")  
    sicks_hours: Mapped[int] = mapped_column(nullable=True)
    sicks_hours_monthly: Mapped[int] = mapped_column( nullable=True)
    number_dependents: Mapped[int] = mapped_column(nullable=True)
    shared_custody: Mapped[bool] = mapped_column(Boolean, default=True)
    number_concessions: Mapped[int] = mapped_column(nullable=True)
    veteran: Mapped[bool] = mapped_column(Boolean, default=True)
    type_payroll: Mapped[str] = mapped_column(String(50), nullable=True)
    schedule_type: Mapped[str] = mapped_column(String(50), nullable=True)
    payment_percentage: Mapped[str] = mapped_column(String(50), nullable=True)

    employee_type: Mapped[str] = mapped_column(String(50), nullable=True)
    social_security_number: Mapped[str] = mapped_column(String(50), nullable=True)
    marital_status: Mapped[int] = mapped_column(
        nullable=True,
    )
    address: Mapped[str] = mapped_column(String(50), nullable=True)
    address_state: Mapped[str] = mapped_column(String(50), nullable=True)
    address_country: Mapped[str] = mapped_column(String(50), nullable=True)
    address_number: Mapped[str] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=True)
    smartphone_number: Mapped[str] = mapped_column(String(50), nullable=True)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=True)
    deleted_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    update_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        onupdate=func.now(),
    )
