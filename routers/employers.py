import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from datetime import  datetime

from controllers.employers_controller import create_employer_controller, delete_employer_controller, employers_controller, get_all_employers_by_company_id_controller, get_employer_by_id_controller, update_employer_controller
from database.config import session
from routers.auth import user_dependency

from models.employers import Employers
from models.companies import Companies
from models.time import Time


from schemas.employee import EmployersSchema
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
employers_router = APIRouter()


@employers_router.post("/{company_id}")
async def create_employer(employer_data: EmployersSchema, company_id : int):        
    return create_employer_controller(employer_data, company_id)



@employers_router.get("/{company_id}")
async def get_all_employers_by_company_id(company_id: int,user: user_dependency):
    return get_all_employers_by_company_id_controller(company_id, user)


@employers_router.get("/{company_id}/{employers_id}")
async def get_employer_by_id(employers_id: int,company_id: int,user: user_dependency):
    return get_employer_by_id_controller(employers_id,company_id,user)


@employers_router.put("/{employers_id}")
async def update_employer(employers_id: int, employer: EmployersSchema, user: user_dependency):
    return update_employer_controller(employers_id, employer, user)


@employers_router.delete("/{employers_id}")
async def employers(employers_id: int, user: user_dependency):
    return employers_controller(employers_id, user_dependency)


@employers_router.delete("/delete/{employers_id}")
async def delete_employer(employers_id: int, user: user_dependency):
   return delete_employer_controller(employers_id, user)











   