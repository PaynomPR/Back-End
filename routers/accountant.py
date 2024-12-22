from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from controllers.accountant_controller import create_accountant_controller, disable_accountant_controller, get_accountant_controller, get_all_accountants_controller, update_accountant_controller ,delete_accountant_controller
from schemas.accountant import Accountants
from passlib.context import CryptContext
from routers.auth import user_dependency

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
accountant_router = APIRouter()



@accountant_router.post("/")
async def create_accountant(accountants_data: Accountants,user: user_dependency):
    return create_accountant_controller(accountants_data, user)


@accountant_router.get("/")
async def get_all_accountants(user: user_dependency):
    return get_all_accountants_controller(user)


@accountant_router.get("/{id}")
async def get_accountant(user: user_dependency,id: int):
    return get_accountant_controller(user,id)

@accountant_router.put("/{id}")
async def update_accountant(accountants_data: Accountants,user: user_dependency,id: int):   
    return update_accountant_controller(accountants_data, user,id)

@accountant_router.delete("/{id}")
async def disable_accountant(user: user_dependency,id: int):
   return disable_accountant_controller(id)

@accountant_router.delete("/delete/{id}")
async def delete_accountant(id: int):
   return delete_accountant_controller(id)
