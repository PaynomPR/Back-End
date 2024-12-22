from fastapi import APIRouter,  Depends, HTTPException
from fastapi import BackgroundTasks
from schemas.codes import CodeSchema
from controllers.code_controllers import create_code_controller, disable_code_controller, get_all_codes_controller, get_code_by_id_controller, update_code_controller


code_router = APIRouter()


@code_router.post("/")
async def create_code(code_data: CodeSchema,background_tasks: BackgroundTasks):
    return create_code_controller(code_data,background_tasks)


@code_router.put("/{code_id}")
async def update_code(code_data: CodeSchema,code_id: int):
    return update_code_controller(code_data, code_id)


@code_router.get("/")
async def get_all_codes():
    return get_all_codes_controller()


@code_router.get("/{code_id}")
async def get_code_by_id(code_id: int):
    return get_code_by_id_controller(code_id)



@code_router.delete("/{id}")
async def disable_code(id: int):
    return disable_code_controller(id)
