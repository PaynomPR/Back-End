
from fastapi import HTTPException, status
from database.config import session
from models.periods import Period, PeriodType
from schemas.period import PeriodRead




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
    from datetime import date, timedelta
    periods = []
    start_date = date(year, 1, 1)
    while start_date.year == year:
        end_date = start_date + timedelta(days=6)
        if end_date.year != year:
            end_date = date(year, 12, 31)
        periods.append({
            "year": year,
            "period_number": len(periods) + 1,
            "period_start": start_date,
            "period_end": end_date,
            "period_type": PeriodType.WEEKLY
        })
        start_date = end_date + timedelta(days=1)
    return create_periods(periods)

def create_biweekly_periods(year: int) -> list[Period]:
    from datetime import date, timedelta
    periods = []
    start_date = date(year, 1, 1)
    while start_date.year == year:
        end_date = start_date + timedelta(days=13)
        if end_date.year != year:
            end_date = date(year, 12, 31)
        periods.append({
            "year": year,
            "period_number": len(periods) + 1,
            "period_start": start_date,
            "period_end": end_date,
            "period_type": PeriodType.BIWEEKLY
        })
        start_date = end_date + timedelta(days=1)
    return create_periods(periods)

def create_monthly_periods(year: int) -> list[Period]:
    from datetime import date, timedelta
    periods = []
    for month in range(1, 13):
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year, 12, 31)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        periods.append({
            "year": year,
            "period_number": month,
            "period_start": start_date,
            "period_end": end_date,
            "period_type": PeriodType.MONTHLY
        })
    return create_periods(periods)


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