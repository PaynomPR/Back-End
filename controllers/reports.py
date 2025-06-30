from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from models import employers, periods, time as time_model, vacation_times
from schemas import reports as report_schemas
from datetime import date
from typing import List, Optional
from database.config import session


report_router = APIRouter()

# --- Helper Functions for Time Calculation ---
def time_to_minutes(time_str: str) -> int:
    if not time_str or ':' not in time_str:
        return 0
    try:
        hours, minutes = map(int, time_str.split(':'))
        return (hours * 60) + minutes
    except (ValueError, TypeError):
        return 0

def minutes_to_time(total_minutes: int) -> str:
    if total_minutes < 0:
        sign = "-"
        total_minutes = abs(total_minutes)
    else:
        sign = ""
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{sign}{hours:02d}:{minutes:02d}"




def get_company_periodical_summary(company_id, start,end):
    """
    Generates a detailed, period-by-period report of vacation and sick time for all employees in a company.
    """
    

    # 1. Get all employees for the company
    all_employees = session.query(employers.Employers).filter(
        employers.Employers.company_id == company_id,
        employers.Employers.is_deleted == False
    ).all()

    if not all_employees:
        raise HTTPException(status_code=404, detail="No active employees found for this company.")

    # 2. Get all periods that fall within the requested date range
    periods_in_range = session.query(periods.Period).filter(
        and_(
            periods.Period.period_start >= start,
            periods.Period.period_end <= end,
            periods.Period.is_deleted == False
        )
    ).order_by(periods.Period.period_start).all()

    if not periods_in_range:
        return []

    company_report = []

    # Loop through each employee
    for emp in all_employees:
        # 3. Get Starting Balance for the current employee
        last_time_record_before = session.query(time_model.Time)\
            .join(periods.Period, time_model.Time.period_id == periods.Period.id)\
            .filter(time_model.Time.employer_id == emp.id, periods.Period.period_end < start)\
            .order_by(periods.Period.period_end.desc())\
            .first()

        if last_time_record_before:
            current_vacation_balance_minutes = time_to_minutes(last_time_record_before.vacation_acum_hours)
            current_sick_balance_minutes = time_to_minutes(last_time_record_before.sicks_acum_hours)
        else:
            # If no record before, use the initial values from the employer model
            current_vacation_balance_minutes = time_to_minutes(emp.vacation_time)
            current_sick_balance_minutes = time_to_minutes(emp.sick_time)

        # 4. Iterate through each period for the current employee
        period_details = []
        for p in periods_in_range:
            # a. Get hours USED in this specific period from VacationTimes (transactions)
            hours_used_result = session.query(
                func.coalesce(func.sum(vacation_times.VacationTimes.vacation_hours), 0).label("total_vacation_used"),
                func.coalesce(func.sum(vacation_times.VacationTimes.sicks_hours), 0).label("total_sick_used")
            ).filter(
                and_(
                    vacation_times.VacationTimes.employer_id == emp.id,
                    vacation_times.VacationTimes.period_id == p.id
                )
            ).one()
            
            vacation_used_minutes = (hours_used_result.total_vacation_used or 0) * 60
            sick_used_minutes = (hours_used_result.total_sick_used or 0) * 60

            # b. Get the ENDING balance for this period from the Time model (payroll snapshot)
            time_record_for_period = session.query(time_model.Time).filter(
                and_(
                    time_model.Time.employer_id == emp.id,
                    time_model.Time.period_id == p.id
                )
            ).first()

            if time_record_for_period:
                vacation_end_balance_minutes = time_to_minutes(time_record_for_period.vacation_acum_hours)
                sick_end_balance_minutes = time_to_minutes(time_record_for_period.sicks_acum_hours)
            else:
                # If no payroll ran, no hours were added. The end balance is the start balance minus usage.
                vacation_end_balance_minutes = current_vacation_balance_minutes - vacation_used_minutes
                sick_end_balance_minutes = current_sick_balance_minutes - sick_used_minutes

            # c. Calculate ADDED hours by deduction: Added = (End - Start) + Used
            vacation_added_minutes = (vacation_end_balance_minutes - current_vacation_balance_minutes) + vacation_used_minutes
            sick_added_minutes = (sick_end_balance_minutes - current_sick_balance_minutes) + sick_used_minutes

            # d. Create the report entry for this period
            period_entry = report_schemas.PerPeriodDetail(
                period_number=p.period_number,
                period_start=p.period_start,
                period_end=p.period_end,
                vacation_start_balance=minutes_to_time(current_vacation_balance_minutes),
                vacation_hours_added=minutes_to_time(vacation_added_minutes),
                vacation_hours_used=minutes_to_time(vacation_used_minutes),
                vacation_end_balance=minutes_to_time(vacation_end_balance_minutes),
                sick_start_balance=minutes_to_time(current_sick_balance_minutes),
                sick_hours_added=minutes_to_time(sick_added_minutes),
                sick_hours_used=minutes_to_time(sick_used_minutes),
                sick_end_balance=minutes_to_time(sick_end_balance_minutes)
            )
            period_details.append(period_entry)

            # e. Update the current balance for the next iteration
            current_vacation_balance_minutes = vacation_end_balance_minutes
            current_sick_balance_minutes = sick_end_balance_minutes

        # 5. Construct the final response object for the employee
        employee_report = report_schemas.EmployeePeriodicalReport(
            employer_id=emp.id,
            first_name=emp.first_name,
            last_name=emp.last_name,
            report_start_date=start,
            report_end_date=end,
            periods=period_details
        )
        company_report.append(employee_report)

    return company_report