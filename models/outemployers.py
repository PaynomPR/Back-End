from typing import List
from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String,Date, Boolean, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from database.config import Base


class  OutEmployers(Base):
    __tablename__ = "outemployers"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    last_name: Mapped[str] = mapped_column(String(50),nullable=True)    
    mother_last_name: Mapped[str] = mapped_column(String(50),nullable=True)    
    first_name: Mapped[str] = mapped_column(String(50),nullable=True)    
    middle_name: Mapped[str] = mapped_column(String(50),nullable=True)  
    company_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("companies.id"), nullable=True, index=True
    )
    company = relationship("Companies", back_populates="outemployers")    
    type_entity: Mapped[int] = mapped_column(nullable=True,)  
    gender: Mapped[int] = mapped_column(nullable=True,)
    birthday: Mapped[TIMESTAMP] = mapped_column(
        Date(), nullable=True
    )  
    regular_pay: Mapped[float] = mapped_column(nullable=True,default=0)  
    account_number: Mapped[str] = mapped_column(String(50),nullable=True) 
    email: Mapped[str] = mapped_column(String(50),nullable=True) 
    fax : Mapped[str] = mapped_column(String(50),nullable=True) 
    website : Mapped[str] = mapped_column(String(50),nullable=True) 
    withholding: Mapped[str] = mapped_column(nullable=True)   
    merchant_register : Mapped[str] = mapped_column(String(50),nullable=True) 
    employer_id: Mapped[str] = mapped_column(String(50),nullable=True) 
    bank_account: Mapped[str] = mapped_column(String(50),nullable=True)  
    time = relationship("TimeOutEmployer", back_populates="employer")
  
    address: Mapped[str] = mapped_column(String(50),nullable=True)    
    address_state: Mapped[str] = mapped_column(String(50),nullable=True)    
    address_country: Mapped[str] = mapped_column(String(50),nullable=True)    
    address_number: Mapped[str] = mapped_column(String(50),nullable=True)    
    phone_number: Mapped[str] = mapped_column(String(50),nullable=True)    
    smartphone_number: Mapped[str] = mapped_column(String(50),nullable=True)    

    

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
