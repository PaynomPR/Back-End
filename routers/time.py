from fastapi import APIRouter


from controllers.time_controller import  create_time_controller, delete_time_controller, get_time_by_employer_id_controller, update_time_controller
from database.config import session
from routers.auth import user_dependency

from models.time import Time
from models.employers import Employers
from models.payments import Payments


from schemas.time import TimeShema, TimeIDShema2
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
time_router = APIRouter()


@time_router.post("/{employer_id}")
async def create_time(time_data: TimeShema, employer_id: int):
    return create_time_controller(time_data, employer_id)


@time_router.get("/{employer_id}")
async def get_time_by_employer_id(employer_id: int):
    return get_time_by_employer_id_controller(employer_id)




@time_router.delete("/{time_id}")
async def delete_time(time_id: int, user: user_dependency):
    return delete_time_controller(time_id, user)


@time_router.put("/{time_id}")
async def update_time(time_id: int, time: TimeIDShema2):
    return update_time_controller(time_id, time)