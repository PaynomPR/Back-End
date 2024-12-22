from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String,Date, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database.config import Base


class  FixedTaxes(Base):
    __tablename__ = "fixed_taxes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50),nullable=False,)
    amount: Mapped[float] = mapped_column(nullable=True,default=0)
    limit: Mapped[int] = mapped_column(nullable=True,default=0)  


class  Taxes(Base):
    __tablename__ = "taxes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50),nullable=False,)
    amount: Mapped[float] = mapped_column(nullable=True,default=0)
    required: Mapped[float] = mapped_column(nullable=True,default=0)
    type_taxe: Mapped[float] = mapped_column(nullable=True,default=0)
    type_amount: Mapped[float] = mapped_column(nullable=True,default=0)

    company_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("companies.id"), nullable=True, index=True
    )
    company = relationship("Companies", back_populates="taxes")

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
