from datetime import date
from sqlalchemy import TIMESTAMP, Date, Integer, Boolean, func, Enum
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from database.config import Base
import enum


class PeriodType(enum.Enum):
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class Period(Base):
    __tablename__ = "periods"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    period_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    period_start: Mapped[date] = mapped_column(Date(), nullable=False, index=True)
    period_end: Mapped[date] = mapped_column(Date(), nullable=False, index=True)
    period_type: Mapped[PeriodType] = mapped_column(Enum(PeriodType), nullable=False)

    time = relationship("Time", back_populates="period")

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
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
