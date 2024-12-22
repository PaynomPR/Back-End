from fastapi import APIRouter, Depends
from controllers.fixed_taxes_controller import create_fixed_taxe_controller, delete_taxe_controller,  get_fixed_taxes_controller, update_taxe_controller, get_fixed_taxes_by_id_controller 
from routers.auth import user_dependency
from controllers.time_controller import get_sum_taxes_by_employer_id_controller
from models.taxes import Taxes
from schemas.fixed_taxes import FixedTaxeIDShema, FixedTaxeShema

fixed_taxes_router = APIRouter()

@fixed_taxes_router.post("/")
async def create_taxe(taxe_data: FixedTaxeShema):    
    return create_fixed_taxe_controller(taxe_data)
    
@fixed_taxes_router.delete("/{taxes_id}")
async def employers(taxes_id: int,):
    return delete_taxe_controller(taxes_id)

@fixed_taxes_router.get("/")
async def get_fixed_taxes():
    return get_fixed_taxes_controller()

@fixed_taxes_router.get("/{taxes_id}")
async def get_fixed_taxes_by_id(taxes_id:int):
    return get_fixed_taxes_by_id_controller(taxes_id)

@fixed_taxes_router.get("/sum_taxes_by_id/{employer_id}")
async def get_sum_taxes_by_id(employer_id:int):
    return get_sum_taxes_by_employer_id_controller(employer_id)



@fixed_taxes_router.put("/{taxe_id}")
async def update_taxe(taxe_id: int, taxe: FixedTaxeIDShema):
    return update_taxe_controller(taxe_id, taxe)



