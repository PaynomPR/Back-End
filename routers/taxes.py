from fastapi import APIRouter, Depends
from controllers.taxes_controller import create_taxe_controller,disable_taxe_controller, delete_taxe_controller, get_taxes_by_company_and_taxe_controller, get_taxes_by_company_controller, update_taxe_controller
from routers.auth import user_dependency
from models.taxes import Taxes
from schemas.taxes import TaxeIDShema, TaxeShema




taxes_router = APIRouter()


@taxes_router.post("/{company_id}")
async def create_taxe(taxe_data: TaxeShema, company_id : int):    
    return create_taxe_controller(taxe_data, company_id)
    

@taxes_router.delete("/{taxes_id}")
async def employers(taxes_id: int,):
    return disable_taxe_controller(taxes_id)

@taxes_router.delete("/delete/{taxes_id}")
async def employers(taxes_id: int,):
    return delete_taxe_controller(taxes_id)

@taxes_router.get("/{company_id}")
async def get_taxes_by_company(company_id: int):
    return get_taxes_by_company_controller(company_id)


@taxes_router.get("/{company_id}/{taxe_id}")
async def get_taxes_by_company(company_id: int,taxe_id:int):
    return get_taxes_by_company_and_taxe_controller(company_id, taxe_id)

@taxes_router.put("/{taxe_id}")
async def update_taxe(taxe_id: int, taxe: TaxeIDShema):
    return update_taxe_controller(taxe_id, taxe)



