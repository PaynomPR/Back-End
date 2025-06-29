from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from database.config import get_db
from models import employers, periods, time as time_model, vacation_times
from schemas import reports as report_schemas
from datetime import date
from typing import List, Optional

router = APIRouter(
    prefix="/reports1",
    tags=["Reports1"]
)

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

@router.get("/vacation-sick-summary", response_model=List[report_schemas.EmployeeReport])
def get_vacation_and_sick_time_report(
    start_date: date,
    end_date: date,
    employer_id: Optional[int] = Query(None, description="Filter by a specific employer ID"),
    db: Session = Depends(get_db)
):
    """
    Generates a report of vacation and sick hours used and accumulated for each employee within a given date range.
    """
    # 1. Base query for employers
    employer_query = db.query(employers.Employers).filter(employers.Employers.is_deleted == False)
    if employer_id:
        employer_query = employer_query.filter(employers.Employers.id == employer_id)
    
    all_employers = employer_query.all()
    if not all_employers:
        raise HTTPException(status_code=404, detail="No active employers found for the given criteria.")

    # 2. Get all periods within the date range
    periods_in_range = db.query(periods.Period).filter(
        and_(
            periods.Period.period_start >= start_date,
            periods.Period.period_end <= end_date,
            periods.Period.is_deleted == False
        )
    ).order_by(periods.Period.period_start).all()

    if not periods_in_range:
        return []

    final_report = []

    for emp in all_employers:
        employee_period_reports = []
        for p in periods_in_range:
            # 3. Calculate hours used from VacationTimes (transactions)
            # We sum the hours for the given employer and period.
            hours_used_result = db.query(
                func.coalesce(func.sum(vacation_times.VacationTimes.vacation_hours), 0).label("total_vacation_used"),
                func.coalesce(func.sum(vacation_times.VacationTimes.sicks_hours), 0).label("total_sick_used")
            ).filter(
                and_(
                    vacation_times.VacationTimes.employer_id == emp.id,
                    vacation_times.VacationTimes.period_id == p.id
                )
            ).one()

            # 4. Get the snapshot of accumulated hours from the Time model (payroll run data)
            time_record = db.query(time_model.Time).filter(
                and_(
                    time_model.Time.employer_id == emp.id,
                    time_model.Time.period_id == p.id
                )
            ).first()

            # We only add a report for the period if there is a payroll record (time_record)
            if time_record:
                period_usage = report_schemas.PeriodUsage(
                    period_number=p.period_number,
                    period_start=p.period_start,
                    period_end=p.period_end,
                    vacation_hours_used=hours_used_result.total_vacation_used,
                    sick_hours_used=hours_used_result.total_sick_used,
                    vacation_hours_accumulated_snapshot=time_record.vacation_acum_hours,
                    sick_hours_accumulated_snapshot=time_record.sicks_acum_hours
                )
                employee_period_reports.append(period_usage)

        if employee_period_reports:
            employee_report = report_schemas.EmployeeReport(
                employer_id=emp.id,
                first_name=emp.first_name,
                last_name=emp.last_name,
                periods_usage=employee_period_reports
            )
            final_report.append(employee_report)

    return final_report

@router.get("/employee-time-summary/{employer_id}", response_model=report_schemas.EmployeeTimeSummary)
def get_employee_time_summary(
    employer_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """
    Generates a summary of an employee's vacation and sick time balances, additions, and usage for a given date range.
    """
    # 1. Get Employee
    emp = db.query(employers.Employers).filter(employers.Employers.id == employer_id, employers.Employers.is_deleted == False).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employer not found")

    # 2. Get Starting Balance (from the last period *before* the start_date)
    last_time_record_before = db.query(time_model.Time)\
        .join(periods.Period, time_model.Time.period_id == periods.Period.id)\
        .filter(time_model.Time.employer_id == emp.id, periods.Period.period_end < start_date)\
        .order_by(periods.Period.period_end.desc())\
        .first()

    if last_time_record_before:
        vacation_start_balance_minutes = time_to_minutes(last_time_record_before.vacation_acum_hours)
        sick_start_balance_minutes = time_to_minutes(last_time_record_before.sicks_acum_hours)
    else:
        # If no record before, use the initial values from the employer
        vacation_start_balance_minutes = time_to_minutes(emp.vacation_time)
        sick_start_balance_minutes = time_to_minutes(emp.sick_time)

    # 3. Get Total Hours Used in the date range from VacationTimes transactions
    periods_in_range_ids = db.query(periods.Period.id).filter(
        and_(
            periods.Period.period_start >= start_date,
            periods.Period.period_end <= end_date,
            periods.Period.is_deleted == False
        )
    ).scalar_subquery()

    hours_used_result = db.query(
        func.coalesce(func.sum(vacation_times.VacationTimes.vacation_hours), 0).label("total_vacation_used"),
        func.coalesce(func.sum(vacation_times.VacationTimes.sicks_hours), 0).label("total_sick_used")
    ).filter(
        and_(
            vacation_times.VacationTimes.employer_id == emp.id,
            vacation_times.VacationTimes.period_id.in_(periods_in_range_ids)
        )
    ).one()
    
    # Note: vacation_hours and sicks_hours in VacationTimes are Mapped[int] (hours), so multiply by 60 for minutes
    vacation_used_minutes = (hours_used_result.total_vacation_used or 0) * 60
    sick_used_minutes = (hours_used_result.total_sick_used or 0) * 60

    # 4. Get Ending Balance (from the last period *within* the date range)
    last_time_record_in_range = db.query(time_model.Time)\
        .join(periods.Period, time_model.Time.period_id == periods.Period.id)\
        .filter(time_model.Time.employer_id == emp.id, periods.Period.period_end <= end_date)\
        .order_by(periods.Period.period_end.desc())\
        .first()

    if last_time_record_in_range:
        vacation_end_balance_minutes = time_to_minutes(last_time_record_in_range.vacation_acum_hours)
        sick_end_balance_minutes = time_to_minutes(last_time_record_in_range.sicks_acum_hours)
    else:
        # If no records in range, end balance is the same as start balance minus used hours
        # This handles cases where an employee might have used hours but no payroll ran yet in the period.
        vacation_end_balance_minutes = vacation_start_balance_minutes - vacation_used_minutes
        sick_end_balance_minutes = sick_start_balance_minutes - sick_used_minutes

    # 5. Calculate Hours Added (deduced from balances and usage)
    # Formula: Added = (End_Balance - Start_Balance) + Used
    vacation_added_minutes = (vacation_end_balance_minutes - vacation_start_balance_minutes) + vacation_used_minutes
    sick_added_minutes = (sick_end_balance_minutes - sick_start_balance_minutes) + sick_used_minutes

    # 6. Construct and return the response object
    response = report_schemas.EmployeeTimeSummary(
        employer_id=emp.id,
        first_name=emp.first_name,
        last_name=emp.last_name,
        start_date=start_date,
        end_date=end_date,
        vacation_start_balance=minutes_to_time(vacation_start_balance_minutes),
        vacation_hours_added=minutes_to_time(vacation_added_minutes),
        vacation_hours_used=minutes_to_time(vacation_used_minutes),
        vacation_end_balance=minutes_to_time(vacation_end_balance_minutes),
        sick_start_balance=minutes_to_time(sick_start_balance_minutes),
        sick_hours_added=minutes_to_time(sick_added_minutes),
        sick_hours_used=minutes_to_time(sick_used_minutes),
        sick_end_balance=minutes_to_time(sick_end_balance_minutes)
    )

    return response

@router.get("/employee-periodical-summary/{employer_id}", response_model=report_schemas.EmployeePeriodicalReport)
def get_employee_periodical_summary(
    employer_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """
    Generates a detailed, period-by-period report of an employee's vacation and sick time.
    """
    # 1. Get Employee
    emp = db.query(employers.Employers).filter(employers.Employers.id == employer_id, employers.Employers.is_deleted == False).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employer not found")

    # 2. Get all periods that fall within the requested date range
    periods_in_range = db.query(periods.Period).filter(
        and_(
            periods.Period.period_start >= start_date,
            periods.Period.period_end <= end_date,
            periods.Period.is_deleted == False
        )
    ).order_by(periods.Period.period_start).all()

    # 3. Get Starting Balance (from the last period *before* the start_date)
    last_time_record_before = db.query(time_model.Time)\
        .join(periods.Period, time_model.Time.period_id == periods.Period.id)\
        .filter(time_model.Time.employer_id == emp.id, periods.Period.period_end < start_date)\
        .order_by(periods.Period.period_end.desc())\
        .first()

    if last_time_record_before:
        current_vacation_balance_minutes = time_to_minutes(last_time_record_before.vacation_acum_hours)
        current_sick_balance_minutes = time_to_minutes(last_time_record_before.sicks_acum_hours)
    else:
        # If no record before, use the initial values from the employer model
        current_vacation_balance_minutes = time_to_minutes(emp.vacation_time)
        current_sick_balance_minutes = time_to_minutes(emp.sick_time)

    # 4. Iterate through each period and build the detailed report
    period_details = []
    for p in periods_in_range:
        # a. Get hours USED in this specific period from VacationTimes (transactions)
        hours_used_result = db.query(
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
        time_record_for_period = db.query(time_model.Time).filter(
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

    # 5. Construct the final response object
    final_report = report_schemas.EmployeePeriodicalReport(
        employer_id=emp.id,
        first_name=emp.first_name,
        last_name=emp.last_name,
        report_start_date=start_date,
        report_end_date=end_date,
        periods=period_details
    )

    return final_report

@router.post("/company-periodical-summary", response_model=List[report_schemas.EmployeePeriodicalReport])
def get_company_periodical_summary(
    request: report_schemas.CompanyPeriodicalReportRequest,
    db: Session = Depends(get_db)
):
    """
    Generates a detailed, period-by-period report of vacation and sick time for all employees in a company.
    """
    company_id = request.company_id
    start_date = request.start_date
    end_date = request.end_date

    # 1. Get all employees for the company
    all_employees = db.query(employers.Employers).filter(
        employers.Employers.company_id == company_id,
        employers.Employers.is_deleted == False
    ).all()

    if not all_employees:
        raise HTTPException(status_code=404, detail="No active employees found for this company.")

    # 2. Get all periods that fall within the requested date range
    periods_in_range = db.query(periods.Period).filter(
        and_(
            periods.Period.period_start >= start_date,
            periods.Period.period_end <= end_date,
            periods.Period.is_deleted == False
        )
    ).order_by(periods.Period.period_start).all()

    if not periods_in_range:
        return []

    company_report = []

    # Loop through each employee
    for emp in all_employees:
        # 3. Get Starting Balance for the current employee
        last_time_record_before = db.query(time_model.Time)\
            .join(periods.Period, time_model.Time.period_id == periods.Period.id)\
            .filter(time_model.Time.employer_id == emp.id, periods.Period.period_end < start_date)\
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
            hours_used_result = db.query(
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
            time_record_for_period = db.query(time_model.Time).filter(
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
            report_start_date=start_date,
            report_end_date=end_date,
            periods=period_details
        )
        company_report.append(employee_report)

    return company_report