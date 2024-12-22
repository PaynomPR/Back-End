from sqlalchemy import TIMESTAMP, ForeignKey, Integer, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, Boolean, func

from database.config import Base


class Accountant(Base):
    __tablename__ = "accountants"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    code_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("codes.id"), nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50))
    first_last_name: Mapped[str] = mapped_column(String(50))
    second_last_name: Mapped[str] = mapped_column(String(50))
    company: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(50))
    country: Mapped[str] = mapped_column(String(50))
    state: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(50))
    zip_code: Mapped[str] = mapped_column(String(50))
    physical_country: Mapped[str] = mapped_column(String(50))
    physical_state: Mapped[str] = mapped_column(String(50))
    physical_address: Mapped[str] = mapped_column(String(50))
    physical_zip_code: Mapped[str] = mapped_column(String(50))
    identidad_ssa: Mapped[str] = mapped_column(String(50))
    identidad_bso: Mapped[str] = mapped_column(String(50))
    identidad_efile: Mapped[str] = mapped_column(String(50))

    
    employer_insurance_number : Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False), nullable=True
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now(), nullable=False
    )
    update_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=True,
        onupdate=func.now(),
    )
