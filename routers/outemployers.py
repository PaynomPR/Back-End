import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from datetime import  datetime


from controllers.outemployers_controller import get_all_company_and_employer_controller, delete_outemployer_controller, create_employer_controller, get_employer_by_id_controller, update_employer_controller
from controllers.outemployers_controller import get_all_outemployers_by_company_id_controller, outemployers_delete_controller

from database.config import session
from routers.auth import user_dependency

from models.outemployers import OutEmployers
from models.companies import Companies
from models.time_outemployer import TimeOutEmployer


from schemas.outemployers import OutEmployersSchema
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outemployers_router = APIRouter()


@outemployers_router.post("/{company_id}")
async def create_employer(employer_data: OutEmployersSchema, company_id : int):    
    return create_employer_controller(employer_data, company_id)

@outemployers_router.get("/time/{company_id}/{employers_id}")
async def get_all_company_and_employer(user: user_dependency,company_id: int,employers_id: int):    
   return get_all_company_and_employer_controller(user,company_id,employers_id)
   
  
@outemployers_router.get("/{company_id}")
async def get_all_outemployers_by_company_id(company_id: int,user: user_dependency):
    return get_all_outemployers_by_company_id_controller(company_id,user)


@outemployers_router.get("/{company_id}/{outemployers_id}")
async def get_employer_by_id(outemployers_id: int,company_id: int,user: user_dependency):
    return get_employer_by_id_controller(outemployers_id,company_id,user)


@outemployers_router.put("/{outemployers_id}")
async def update_employer(outemployers_id: int, employer: OutEmployersSchema, user: user_dependency):
    return update_employer_controller(outemployers_id, employer, user)


@outemployers_router.delete("/{outemployers_id}")
async def outemployers(outemployers_id: int, user: user_dependency):
    return outemployers_delete_controller(outemployers_id, user)

@outemployers_router.delete("/delete/{employers_id}")
async def delete_employer(employers_id: int, user: user_dependency):
    return delete_outemployer_controller(employers_id, user)
    
   
