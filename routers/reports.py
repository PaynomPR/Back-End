from datetime import datetime
import pathlib


from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel

from controllers.reports_controller import counterfoil_by_range_controller,all_counterfoil_controller, counterfoil_controller, form_940_pdf_controller, form_choferil_pdf_controller, form_unemployment_pdf_controller, form_withheld_499_pdf_controller, get_report_cfse_pdf_controller, form_w2pr_pdf_controller, form_941_pdf_controller, form_943_pdf_controller ,counterfoil_by_period_controller, form_wages_txt_controller ,get_w2p_txt_controller , form_bonus_pdf_controller ,get_w2psse_txt_controller , get_report_bonus_pdf_controller
from database.config import session
from models.companies import Companies
from models.employers import Employers
from models.periods import Period
from models.time import Time

from utils.pdfkit.pdfhandled import create_pdf


report_router = APIRouter()

class CompanyYear(BaseModel):
    company_id: int
    year: int
    period: int | None

class CompanyW2P(BaseModel):
    company_id: int
    year: int
    reimbursed: int  
    code: str  


class Bonus(BaseModel):
    amount_max: int
    amount_min: int
    max_employers: int  
    min_employers: int 
    percent_to_max: int 
    percent_to_min: int 
    reg: bool
    over: bool
    vacations: bool
    sick: bool

class CompanyBonus(BaseModel):
    company_id: int
    year: int
     
    bonus: Bonus  



class EmployerYear(BaseModel):
    employer_id: int
    year: int
    period: int | None

class CompanyOrEmployer(BaseModel):
    company_id: int | None
    employer_id: int | None
    year: int

class CompanyRange(BaseModel):
    company_id: int | None
    employer_id: int | None
    start: datetime
    end: datetime



@report_router.get("/counterfoil1/{company_id}/{period_id}")
async def all_counterfoil(company_id: int, period_id: int):
    return all_counterfoil_controller(company_id, period_id)





@report_router.post("/counterfoil/range")
async def counterfoil_by_range(companyRange: CompanyRange):
    return counterfoil_by_range_controller(companyRange.company_id, companyRange.employer_id,companyRange.start,companyRange.end)

@report_router.get("/counterfoil/{company_id}/{employer_id}/period/{period_id}")
async def counterfoil_by_period(company_id: int, employer_id: int, period_id: int):
    return counterfoil_by_period_controller(company_id, employer_id, period_id)

@report_router.get("/counterfoil/{company_id}/{employer_id}/{time_id}")
async def counterfoil(company_id: int, employer_id: int, time_id: int):
    return counterfoil_controller(company_id, employer_id, time_id)


@report_router.post("/form_940_pdf")
async def form_940_pdf(companyYear: CompanyYear):
    return form_940_pdf_controller(companyYear.company_id, companyYear.year)

@report_router.post("/wages_txt")
async def form_wages_txt(companyYear: CompanyYear):
    return form_wages_txt_controller(companyYear.company_id, companyYear.year, companyYear.period)

@report_router.post("/form_941_pdf")
async def form_941_pdf(companyYear: CompanyYear):
    return form_941_pdf_controller(companyYear.company_id, companyYear.year, companyYear.period)

@report_router.post("/bonus_pdf")
async def form_943_pdf(companyBonus: CompanyBonus):
    return get_report_bonus_pdf_controller(companyBonus.company_id, companyBonus.year, companyBonus.bonus)

@report_router.post("/form_943_pdf")
async def form_943_pdf(companyYear: CompanyYear):
    return form_943_pdf_controller(companyYear.company_id, companyYear.year)

@report_router.post("/form_w2pr_pdf")
async def form_w2pr_pdf(companyOrEmployer: CompanyOrEmployer):
    return form_w2pr_pdf_controller(companyOrEmployer.company_id, companyOrEmployer.employer_id, companyOrEmployer.year)


@report_router.post("/form_unemplo")
async def form_unemployment_pdf(companyYear: CompanyYear):
    return form_unemployment_pdf_controller(companyYear.company_id, companyYear.year, companyYear.period)


@report_router.post("/form_withheld_499_pdf")
async def form_withheld_499_pdf(companyYear: CompanyYear):
    return form_withheld_499_pdf_controller(companyYear.company_id, companyYear.year, companyYear.period)



@report_router.post("/form_choferil_pdf")
async def form_choferil_pdf(companyYear: CompanyYear):
    return form_choferil_pdf_controller(companyYear.company_id, companyYear.year, companyYear.period)

@report_router.post("/get_report_cfse_pdf")
async def get_report_cfse_pdf(companyYear: CompanyYear):
    return get_report_cfse_pdf_controller(companyYear.company_id, companyYear.year, companyYear.period)

@report_router.post("/get_w2p_txt")
async def get_w2p_txt(CompanyW2P: CompanyW2P):
    return get_w2p_txt_controller(CompanyW2P.company_id, CompanyW2P.year,CompanyW2P.reimbursed,CompanyW2P.code)

@report_router.post("/get_w2psse_txt")
async def get_w2pSSE_txt(CompanyW2P: CompanyW2P):
    return get_w2psse_txt_controller(CompanyW2P.company_id, CompanyW2P.year,CompanyW2P.reimbursed,CompanyW2P.code)