from sqlalchemy import TIMESTAMP, Date, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database.config import Base


class Companies(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    commercial_register: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    registration_date: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=True,
        onupdate=func.now(),
    )
    jurisdiction: Mapped[str] = mapped_column(String(50))
    code_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("codes.id"), nullable=False, index=True
    )
    date_close: Mapped[TIMESTAMP] = mapped_column(Date(), nullable=True)
    coml: Mapped[TIMESTAMP] = mapped_column(Date(), nullable=True)
    number_patronal: Mapped[str] = mapped_column(String(50))
    accountant_id: Mapped[int] = mapped_column(
        nullable=True,
    )
    employers = relationship("Employers", back_populates="company")
    outemployers = relationship("OutEmployers", back_populates="company")
    taxes = relationship("Taxes", back_populates="company")
    choferil_number: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50))
    contact: Mapped[str] = mapped_column(String(50))
    contact_number: Mapped[str] = mapped_column(String(50))
    website: Mapped[str] = mapped_column(String(50))
    postal_address: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    vacation_hours: Mapped[float] = mapped_column(nullable=True)
    vacation_date: Mapped[float] = mapped_column( nullable=True)
    sicks_hours: Mapped[float] = mapped_column(nullable=True)
    sicks_date: Mapped[float] = mapped_column( nullable=True)
    zipcode_postal_address: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    country_postal_address: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    state_postal_addess: Mapped[str] = mapped_column(String(50))
    physical_address: Mapped[str] = mapped_column(String(50))
    w2_first_control: Mapped[str] = mapped_column(String(50))
    w2_last_control: Mapped[str] = mapped_column(String(50))
    sp_first_control: Mapped[str] = mapped_column(String(50))
    sp_last_control: Mapped[str] = mapped_column(String(50))
    zipcode_physical_address: Mapped[str] = mapped_column(String(50))
    country_physical_address: Mapped[str] = mapped_column(String(50))
    state_physical_address: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(50))
    fax_number: Mapped[str] = mapped_column(String(50))
    industrial_code: Mapped[str] = mapped_column(String(50))
    payer: Mapped[str] = mapped_column(String(50))
    desem: Mapped[str] = mapped_column(String(50))
    special_contribution: Mapped[str] = mapped_column(String(50), nullable=True,default="1")

    employed_contribution: Mapped[str] = mapped_column(String(50))

    disabled_percent: Mapped[str] = mapped_column(String(50))
    unemployment_percentage: Mapped[str] = mapped_column(String(50))
    polize_number: Mapped[str] = mapped_column(String(50))
    driver_code: Mapped[str] = mapped_column(String(50))
    driver_rate: Mapped[str] = mapped_column(String(50))

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False), nullable=True
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now()
    )
    update_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=True,
        onupdate=func.now(),
    )
    tax_authority_first_control:Mapped[int] = mapped_column( nullable=True)
    tax_authority_second_control:Mapped[int] = mapped_column( nullable=True)