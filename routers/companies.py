import bcrypt
from datetime import datetime

from sqlalchemy.orm import aliased

from fastapi import APIRouter
from controllers.companies_controller import (
    create_company_controller,
    delete_company_controller,
    disable_company_controller,
    get_all_companies_controller,
    get_all_company_and_employer_controller,
    get_companies_by_id_controller,
    get_company_controller,
    get_talonario_controller,
    update_company_controller,
    get_talonario_by_company_controller
    
)
from controllers.time_controller import get_all_data_time_employer_controller
from database.config import session
from schemas.companies import CompaniesSchema, CompaniesWithEmployersSchema
from sqlalchemy.orm import Session

from models.companies import Companies
from models.employers import Employers
from models.taxes import Taxes
from sqlalchemy.orm import joinedload

from models.time import Time
from models.payments import Payments

from routers.auth import user_dependency

companies_router = APIRouter()

# Crear una nueva compañía
@companies_router.post("/")
async def create_company(companie_data: CompaniesSchema, user: user_dependency):
    return create_company_controller(companie_data, user)

# Obtener todas las compañías
@companies_router.get("/")
async def get_all_companies(user: user_dependency):
    
    return get_all_companies_controller(user)

# Obtener compañía y empleador por ID
@companies_router.get("/{company_id}/employer/{employers_id}/year/{year}")
async def get_all_company_and_employer(user: user_dependency, company_id: int, employers_id: int,year : str):
    return get_all_company_and_employer_controller(user, company_id, employers_id,year)

# Obtener talonario por compañía, empleador y periodo
@companies_router.get("/{company_id}/employer/{employers_id}/period/{period_id}")
async def get_talonario(user: user_dependency, company_id: int, employers_id: int, period_id: int):
    return get_talonario_controller(user, company_id, employers_id, period_id)


@companies_router.get("/{company_id}/employer/{employer_id}/time/{time_id}")
async def get_all_data_time_employer(company_id: int,employer_id: int,time_id: int):
    return get_all_data_time_employer_controller(company_id,employer_id,time_id)
# Obtener una compañía específica por su ID
@companies_router.get("/{companies_id}")
async def get_companies_by_id(companies_id: int):
    return get_companies_by_id_controller(companies_id)

# Obtener compañía específica y sus empleadores
@companies_router.get("/employers/{companies_id}")
async def get_company(user: user_dependency, companies_id: int):
    return get_company_controller(user, companies_id)

# Actualizar una compañía específica
@companies_router.put("/{companies_id}")
async def update_company(companies_id: int, company_data: CompaniesSchema):
    return update_company_controller(companies_id, company_data)

# Deshabilitar una compañía específica
@companies_router.delete("/{id}")
async def disable_company(id: int):
    return disable_company_controller(id)

# Eliminar una compañía específica
@companies_router.delete("/delete/{id}")
async def delete_company(id: int):
    return delete_company_controller(id)

# Obtener talonario por compañía y periodo
@companies_router.get("/{company_id}/period/{period_id}")
async def get_talonario_by_company(user: user_dependency, company_id: int, period_id: int):
    return get_talonario_by_company_controller(user, company_id,  period_id)
