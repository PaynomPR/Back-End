import bcrypt
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from starlette import status
from datetime import  datetime

from database.config import session
from routers.auth import user_dependency

from models.taxes import Taxes
from models.payments import Payments



from schemas.taxes import TaxeIDShema, TaxeShema
from passlib.context import CryptContext



taxes_router = APIRouter()



def create_taxe_controller(taxe_data, company_id):
    try:
        taxes_query = Taxes(        
            name = taxe_data.name,
            amount = taxe_data.amount,
            company_id = company_id, 
            is_deleted = False,  
            required = taxe_data.required,  
            type_taxe = taxe_data.type_taxe,  
            type_amount = taxe_data.type_amount,  

        )     
        
        session.add(taxes_query)
        session.commit()
        session.refresh(taxes_query)   
        return {"ok": True, "msg": "Taxes was successfully created", "result": taxes_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def disable_taxe_controller(taxes_id):
    try:    
        taxe_query = session.query(Taxes).filter(Taxes.id == taxes_id).first()
        taxe_query.is_deleted = not taxe_query.is_deleted    
        taxe_query.deleted_at = datetime.utcnow()
        session.add(taxe_query)   
        session.commit()  
        session.refresh(taxe_query)   
        return {"ok": True, "msg": "Taxe eliminado con exito", "result": taxe_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def get_taxes_by_company_controller(company_id):
    try:
        taxe_query = session.query(Taxes).filter(Taxes.company_id == company_id).all()

        return {
            "ok": True,
            "msg": "Taxe se recuperaron con éxito",
            "result": taxe_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def get_taxes_by_company_and_taxe_controller(company_id, taxe_id):
    try:
        taxe_query = session.query(Taxes).filter(Taxes.company_id == company_id,Taxes.id == taxe_id).first()

        return {
            "ok": True,
            "msg": "Taxe se recuperaron con éxito",
            "result": taxe_query,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def update_taxe_controller(taxe_id, taxe):
    try:
        taxes_query = session.query(Taxes).filter(Taxes.id==taxe_id).first()
            
        taxes_query.name = taxe.name,
        taxes_query.amount = taxe.amount,   
        taxes_query.required = taxe.required,  
        taxes_query.type_taxe = taxe.type_taxe,  

        taxes_query.type_amount = taxe.type_amount,  

        session.add(taxes_query)
        session.commit()
        session.refresh(taxes_query)

        return {"ok": True, "msg": "Taxe se actualizo con exito", "result": taxes_query}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Se ha producido un error {str(e)}"
        )
    finally:
        session.close()

def delete_taxe_controller(taxe_id):
    try: 
        # Verificar si la compañía tiene time asociados
        taxe_count = session.query(Payments).filter(Payments.taxe_id == taxe_id).count()

        if taxe_count > 0:   
            return {"ok": False, "msg": "El Taxe no puede ser eliminado porque esta cargado en horas de usuarios.", "result": None}
        # Si no hay empleados, proceder con la eliminación
        taxe_query = session.query(Taxes).filter(Taxes.id == taxe_id).first()
        if taxe_query:
            session.delete(taxe_query)
            session.commit()
            return {"ok": True, "msg": "Taxe eliminada con éxito.", "result": taxe_query}
        else:
            return {"ok": False, "msg": "Taxe no encontrada.", "result": None}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
    finally:
        session.close()