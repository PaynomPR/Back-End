from pydantic import BaseModel
from datetime import date
from typing import List

class PeriodUsage(BaseModel):
    period_number: int
    period_start: date
    period_end: date
    vacation_hours_used: int
    sick_hours_used: int
    vacation_hours_accumulated_snapshot: str
    sick_hours_accumulated_snapshot: str

    class Config:
        orm_mode = True

class EmployeeReport(BaseModel):
    employer_id: int
    first_name: str
    last_name: str
    periods_usage: List[PeriodUsage]

    class Config:
        orm_mode = True

class PerPeriodDetail(BaseModel):
    period_number: int
    period_start: date
    period_end: date
    vacation_start_balance: str
    vacation_hours_added: str
    vacation_hours_used: str
    vacation_end_balance: str
    sick_start_balance: str
    sick_hours_added: str
    sick_hours_used: str
    sick_end_balance: str

class EmployeePeriodicalReport(BaseModel):
    employer_id: int
    first_name: str
    last_name: str
    report_start_date: date
    report_end_date: date
    periods: List[PerPeriodDetail]

    class Config:
        orm_mode = True

class CompanyPeriodicalReportRequest(BaseModel):
    company_id: int
    start_date: date
    end_date: date