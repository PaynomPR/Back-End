from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from database.config import session
from models.periods import Period, PeriodType
from controllers.period import create_weekly_periods, create_biweekly_periods, create_monthly_periods

def periods_exist(year: int, period_type: PeriodType) -> bool:
    return session.query(Period).filter(Period.year==year, Period.period_type==period_type).first() is not None

def initialize_periods():

    # Create periods for the current year and the previous year
    current_year = date.today().year
    previous_year = current_year - 1


    if not periods_exist(previous_year, PeriodType.WEEKLY):
        create_weekly_periods(previous_year)
    if not periods_exist(current_year, PeriodType.WEEKLY):
        create_weekly_periods(current_year)
    if not periods_exist(previous_year, PeriodType.BIWEEKLY):
        create_biweekly_periods(previous_year)
    if not periods_exist(current_year, PeriodType.BIWEEKLY):
        create_biweekly_periods(current_year)
    if not periods_exist(previous_year, PeriodType.MONTHLY):
        create_monthly_periods(previous_year)
    if not periods_exist(current_year, PeriodType.MONTHLY):
        create_monthly_periods(current_year)

    session.commit()
    # print("Periods initialized successfully")

