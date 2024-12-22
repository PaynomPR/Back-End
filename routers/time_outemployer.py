import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends
from starlette.responses import FileResponse
from fastapi import  Response

from controllers.time_outemployer_controller import create_time_controller, get_time_by_employer_id_controller, delete_employer_controller, update_time_controller
from database.config import session
from routers.auth import user_dependency

from models.time_outemployer import TimeOutEmployer
from models.outemployers import OutEmployers
from models.companies import Companies





from schemas.time_outemployer import OutTimeIDShema, OutTimeShema, OutTimeIDShema2
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outtime_router = APIRouter()



@outtime_router.post("/{employer_id}")
async def create_time(time_data: OutTimeShema, employer_id : int):    
    return create_time_controller(time_data, employer_id)

@outtime_router.get("/{employer_id}")
async def get_time_by_employer_id(employer_id: int):
    return get_time_by_employer_id_controller(employer_id)


@outtime_router.delete("/{time_id}")
async def delete_employer(time_id: int, user: user_dependency):
    delete_employer_controller(time_id, user)
 

@outtime_router.put("/{time_id}")
async def update_time(time_id: int, time: OutTimeIDShema2):
    return update_time_controller(time_id, time)

