from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String,Date, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database.config import Base



class  TimeOutEmployer(Base):
    __tablename__ = "time_outemployer"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    regular_hours: Mapped[str] = mapped_column(nullable=True,default=0)
    regular_min: Mapped[str] = mapped_column(nullable=True,default=0)
    regular_pay: Mapped[float] = mapped_column(nullable=True,default=0)
    detained: Mapped[float] = mapped_column(nullable=True,default=0)

    employer_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("outemployers.id"), nullable=True, index=True
    )
    employer = relationship("OutEmployers", back_populates="time")

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
