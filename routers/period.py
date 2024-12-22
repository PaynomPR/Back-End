from fastapi import APIRouter, Depends
from controllers.period import create_weekly_periods, create_biweekly_periods, create_monthly_periods, get_all_periods_controller, get_periods_by_year_and_type_controller
from models.periods import PeriodType
from schemas.period import PeriodCreate, PeriodRead

period_routes = APIRouter()


@period_routes.post("/weekly/", response_model=list[PeriodRead])
def create_weekly_periods_route(year: int):
    return create_weekly_periods(year)

@period_routes.post("/biweekly/", response_model=list[PeriodRead])
def create_biweekly_periods_route(year: int):
    return create_biweekly_periods(year)

@period_routes.post("/monthly/", response_model=list[PeriodRead])
def create_monthly_periods_route(year: int):
    return create_monthly_periods(year)

### get all periods 
@period_routes.get("/periods", response_model=list[PeriodRead])
def get_all_period():
    return get_all_periods_controller()


@period_routes.get("/periods_by_year_and_type/{year}/{period_type}",response_model=list[PeriodRead])
def get_periods_by_year_and_type(year: int, period_type: PeriodType):
    return get_periods_by_year_and_type_controller(year, period_type)


