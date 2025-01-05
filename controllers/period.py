
from fastapi import HTTPException, status
from database.config import session
from models.periods import Period, PeriodType
from schemas.period import PeriodRead
from datetime import date, timedelta




def create_periods(periods_data: list[dict]) -> list[Period]:
    try:
        periods = []
        for period_data in periods_data:
            period = Period(**period_data)
            session.add(period)
            session.commit()
            session.refresh(period)
            periods.append(period)
        return periods
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def create_weekly_periods(year: int) -> list[Period]:
    try:
        last_period = session.query(Period).filter(Period.year == year, Period.period_type == PeriodType.WEEKLY).order_by(Period.period_end.desc()).first()

        if last_period:
            start_date = last_period.period_end + timedelta(days=1)
        else:
            start_date = date(year, 1, 1)

        periods = []
        while start_date.year == year:
            end_date = start_date + timedelta(days=6)
            if end_date.year != year:
                end_date = date(year, 12, 31)
            periods.append({
                "year": year,
                "period_number": (last_period.period_number if last_period else 0) + len(periods) + 1,
                "period_start": start_date,
                "period_end": end_date,
                "period_type": PeriodType.WEEKLY
            })
            start_date = end_date + timedelta(days=1)
        return create_periods(periods)  # Assuming create_periods function exists as in the original code
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}")
    finally:
        session.close()


def create_biweekly_periods(year: int) -> list[Period]:
    try:
        last_period = session.query(Period).filter(Period.year == year, Period.period_type == PeriodType.BIWEEKLY).order_by(Period.period_end.desc()).first()

        if last_period:
            start_date = last_period.period_end + timedelta(days=1)
        else:
            start_date = date(year, 1, 1)

        periods = []
        while start_date.year == year:
            end_date = start_date + timedelta(days=13)
            if end_date.year != year:
                end_date = date(year, 12, 31)
            periods.append({
                "year": year,
                "period_number": (last_period.period_number if last_period else 0) + len(periods) + 1,
                "period_start": start_date,
                "period_end": end_date,
                "period_type": PeriodType.BIWEEKLY
            })
            start_date = end_date + timedelta(days=1)

        return create_periods(periods)

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def create_monthly_periods(year: int) -> list[Period]:
    try:
        last_period = session.query(Period).filter(Period.year == year, Period.period_type == PeriodType.MONTHLY).order_by(Period.period_end.desc()).first()

        if last_period:
            start_date = last_period.period_end + timedelta(days=1)
            start_month = start_date.month 
        else:
            start_date = date(year, 1, 1)
            start_month = 1

        periods = []
        for month in range(start_month, 13):  
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year, 12, 31)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)
            periods.append({
                "year": year,
                "period_number": (last_period.period_number if last_period else 0) + len(periods) + 1,
                "period_start": start_date,
                "period_end": end_date,
                "period_type": PeriodType.MONTHLY
            })

        return create_periods(periods)

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()


def get_all_periods_controller()-> list[PeriodRead]:
    try:
        periods = session.query(Period).all()
        return [PeriodRead.from_orm(period) for period in periods]
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def generate_periods_controller(_year: int = None):   
    
    
    
    create_weekly_periods(_year)
    create_biweekly_periods(_year)
    create_monthly_periods(_year) 
    return {"ok": False, "msg": "Periodos generados", "result": None}

def get_periods_by_year_and_type_controller(year: int, period_type: PeriodType) -> list[PeriodRead]:
    try:
        periods = session.query(Period).filter(
            Period.year == year,
            Period.period_type == period_type,
            Period.is_deleted == False  # Assuming is_deleted is a boolean column
        ).all()
        return [PeriodRead.from_orm(period) for period in periods]
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error mientras se obtienen los períodos: {str(e)}"
        )
    finally:
        session.close()